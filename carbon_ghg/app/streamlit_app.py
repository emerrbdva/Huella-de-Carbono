"""
Aplicación Web Streamlit para Cálculo de Huella de Carbono.
Sistema profesional alineado con GHG Protocol (Scopes 1, 2, 3).
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import logging
import sys
from pathlib import Path

# Agregar el directorio raíz al path de Python
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

# Imports del proyecto
from utils.factors import load_uk_gov_factors, find_factor
from utils.data_validator import validate_activity_data, get_data_quality_summary
from utils.report_generator import (
    generate_excel_report, generate_word_report, check_dependencies
)
from calculators.core import (
    compute_emission, aggregate_emissions_by_scope,
    aggregate_emissions_by_category, get_total_emissions
)
from models.emissions import (
    ActivityRecord, EmissionFactor, EmissionResult,
    SCOPE_1_CATEGORIES, SCOPE_2_CATEGORIES, SCOPE_3_CATEGORIES
)

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===== FUNCIONES DE CACHE PARA OPTIMIZACIÓN =====

@st.cache_data(ttl=3600)  # Cache por 1 hora
def load_factors_cached(file_path: str) -> pd.DataFrame:
    """
    Carga factores de emisión con cache.
    
    OPTIMIZACIÓN: Evita recargar el archivo Excel en cada interacción.
    Cache de 1 hora (3600 segundos).
    
    Args:
        file_path: Ruta al archivo de factores
        
    Returns:
        DataFrame con factores de emisión
    """
    logger.info(f"Cargando factores desde {file_path} (sin cache)")
    return load_uk_gov_factors(file_path)


@st.cache_data(ttl=600)  # Cache por 10 minutos
def compute_all_emissions_cached(
    activities: list,
    factors_df: pd.DataFrame,
    auto_convert: bool = True
) -> list:
    """
    Calcula todas las emisiones con cache.
    
    OPTIMIZACIÓN: Evita recalcular emisiones en cada cambio de tab.
    Cache de 10 minutos (600 segundos).
    
    Args:
        activities: Lista de ActivityRecord
        factors_df: DataFrame con factores
        auto_convert: Auto-conversión de unidades
        
    Returns:
        Lista de EmissionResult
    """
    logger.info(f"Calculando {len(activities)} emisiones (sin cache)")
    results = []
    
    for activity in activities:
        try:
            factor_result = find_factor(
                factors_df,
                activity.category,
                activity.activity_unit,
                geography=activity.geography,
                scope=activity.scope
            )
            
            if factor_result:
                factor_value, factor_source, metadata = factor_result
                
                ef = EmissionFactor(
                    source="UK2025",
                    gas="CO2e",
                    value=factor_value,
                    unit=metadata['unit'],
                    year=metadata['year'],
                    geography=metadata.get('geography'),
                    scope=activity.scope,
                    category=activity.category,
                    notes=metadata.get('full_description')
                )
                
                result = compute_emission(activity, ef, auto_convert_units=auto_convert)
                results.append(result)
        except Exception as e:
            logger.error(f"Error calculating {activity.entity_id}: {e}")
            continue
    
    return results


@st.cache_data(ttl=300)  # Cache por 5 minutos
def create_sankey_chart(results: list) -> go.Figure:
    """
    Crea diagrama Sankey con cache.
    
    OPTIMIZACIÓN: Evita regenerar visualización pesada.
    Cache de 5 minutos (300 segundos).
    
    Args:
        results: Lista de EmissionResult
        
    Returns:
        Figura Plotly con diagrama Sankey
    """
    logger.info("Generando diagrama Sankey (sin cache)")
    
    # Preparar datos para Sankey
    sankey_data = []
    
    for scope in [1, 2, 3]:
        scope_results = [r for r in results if r.activity_record.scope == scope]
        if not scope_results:
            continue
        
        cat_totals = {}
        for r in scope_results:
            cat = r.category_label
            if cat not in cat_totals:
                cat_totals[cat] = {'total': 0, 'entities': {}}
            cat_totals[cat]['total'] += r.emission_tCO2e
            
            entity = r.activity_record.entity_id
            if entity not in cat_totals[cat]['entities']:
                cat_totals[cat]['entities'][entity] = 0
            cat_totals[cat]['entities'][entity] += r.emission_tCO2e
        
        for cat, data in cat_totals.items():
            sankey_data.append({
                'source': f'Scope {scope}',
                'target': cat,
                'value': data['total']
            })
            
            for entity, value in data['entities'].items():
                sankey_data.append({
                    'source': cat,
                    'target': entity,
                    'value': value
                })
    
    if not sankey_data:
        return None
    
    all_nodes = list(set([d['source'] for d in sankey_data] + [d['target'] for d in sankey_data]))
    node_dict = {node: idx for idx, node in enumerate(all_nodes)}
    
    node_colors = []
    for node in all_nodes:
        if 'Scope 1' in node:
            node_colors.append('#FF6B6B')
        elif 'Scope 2' in node:
            node_colors.append('#4ECDC4')
        elif 'Scope 3' in node:
            node_colors.append('#95E1D3')
        elif any(scope in node for scope in ['Scope']):
            node_colors.append('#FFD93D')
        else:
            node_colors.append('#C7CEEA')
    
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color='black', width=0.5),
            label=all_nodes,
            color=node_colors
        ),
        link=dict(
            source=[node_dict[d['source']] for d in sankey_data],
            target=[node_dict[d['target']] for d in sankey_data],
            value=[d['value'] for d in sankey_data],
            color='rgba(0,0,0,0.2)'
        )
    )])
    
    fig.update_layout(
        title="Flujo de Emisiones: Scope → Categoría → Entidad",
        font=dict(size=10),
        height=600
    )
    
    return fig


@st.cache_data(ttl=300)  # Cache por 5 minutos
def create_treemap_chart(results: list) -> go.Figure:
    """
    Crea Treemap con cache.
    
    OPTIMIZACIÓN: Evita regenerar visualización pesada.
    Cache de 5 minutos (300 segundos).
    
    Args:
        results: Lista de EmissionResult
        
    Returns:
        Figura Plotly con Treemap
    """
    logger.info("Generando Treemap (sin cache)")
    
    treemap_data = []
    for r in results:
        treemap_data.append({
            'Scope': f'Scope {r.activity_record.scope}',
            'Categoría': r.category_label,
            'Entidad': r.activity_record.entity_id,
            'Actividad': f"{r.activity_record.activity_value} {r.activity_record.activity_unit}",
            'Emisión (tCO2e)': r.emission_tCO2e,
            'Fuente': r.emission_factor.source
        })
    
    if not treemap_data:
        return None
    
    treemap_df = pd.DataFrame(treemap_data)
    
    fig = px.treemap(
        treemap_df,
        path=['Scope', 'Categoría', 'Entidad'],
        values='Emisión (tCO2e)',
        color='Emisión (tCO2e)',
        color_continuous_scale='RdYlGn_r',
        title='Distribución Jerárquica de Emisiones',
        hover_data={'Actividad': True, 'Fuente': True}
    )
    
    fig.update_layout(
        height=600,
        margin=dict(t=50, l=25, r=25, b=25)
    )
    
    fig.update_traces(
        textinfo="label+value+percent parent",
        hovertemplate='<b>%{label}</b><br>Emisiones: %{value:.2f} tCO2e<br>%{percentParent}<br>%{customdata[0]}<extra></extra>'
    )
    
    return fig


# Configuración de página
st.set_page_config(
    page_title="Calculadora Huella de Carbono - GHG Protocol",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #2E7D32;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E7D32;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        border-radius: 0.5rem;
    }
    .warning-box {
        padding: 1rem;
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        border-radius: 0.5rem;
    }
    .error-box {
        padding: 1rem;
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ===== TÍTULO Y DESCRIPCIÓN =====
st.markdown('<p class="main-header">🌱 Calculadora de Huella de Carbono</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-header">Sistema profesional basado en GHG Protocol | Alcances 1, 2 y 3</p>',
    unsafe_allow_html=True
)

# ===== SIDEBAR: CONFIGURACIÓN =====
st.sidebar.title("⚙️ Configuración")
st.sidebar.markdown("---")

# Inicializar session_state
if 'factors_df' not in st.session_state:
    st.session_state.factors_df = None
if 'activity_df' not in st.session_state:
    st.session_state.activity_df = None
if 'valid_activities' not in st.session_state:
    st.session_state.valid_activities = []
if 'validation_report' not in st.session_state:
    st.session_state.validation_report = None
if 'results' not in st.session_state:
    st.session_state.results = []

# ===== PASO 1: CARGAR FACTORES DE EMISIÓN =====
st.sidebar.header("📁 Paso 1: Factores de Emisión")

factor_source = st.sidebar.selectbox(
    "Fuente de factores",
    ["UK Government 2025", "IPCC 2006", "EPA 2024", "Personalizado"]
)

factors_file = st.sidebar.file_uploader(
    "Sube archivo de factores (Excel)",
    type=["xlsx", "xls"],
    help="UK Gov: ghg-conversion-factors-2025-full-set.xlsx"
)

if factors_file:
    with st.spinner("🔄 Cargando factores de emisión..."):
        try:
            year = 2025 if "2025" in factor_source else 2024
            # Usar versión cacheada para mejor rendimiento
            st.session_state.factors_df = load_factors_cached(factors_file.name, year=year)
            st.sidebar.success(f"✅ {len(st.session_state.factors_df)} factores cargados (cached)")
        except Exception as e:
            st.sidebar.error(f"❌ Error: {str(e)}")
            st.session_state.factors_df = None
            logger.error(f"Error loading factors: {e}")

# ===== PASO 2: CARGAR DATOS DE ACTIVIDAD =====
st.sidebar.markdown("---")
st.sidebar.header("📊 Paso 2: Datos de Actividad")

activity_file = st.sidebar.file_uploader(
    "Sube tus datos (CSV/Excel)",
    type=["csv", "xlsx", "xls"],
    help="Debe incluir: entity_id, scope, category, activity_value, activity_unit"
)

if activity_file:
    try:
        if activity_file.name.endswith(".csv"):
            st.session_state.activity_df = pd.read_csv(activity_file)
        else:
            st.session_state.activity_df = pd.read_excel(activity_file)
        st.sidebar.success(f"✅ {len(st.session_state.activity_df)} filas cargadas")
    except Exception as e:
        st.sidebar.error(f"❌ Error: {str(e)}")
        st.session_state.activity_df = None

# ===== OPCIONES AVANZADAS =====
st.sidebar.markdown("---")
st.sidebar.header("🔧 Opciones Avanzadas")

auto_unit_conversion = st.sidebar.checkbox("Conversión automática de unidades", value=True)
strict_validation = st.sidebar.checkbox("Validación estricta", value=False)
include_market_based = st.sidebar.checkbox("Scope 2: Incluir Market-Based", value=False)

# ===== ÁREA PRINCIPAL =====

# Tabs para organizar la interfaz
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Datos", "🔍 Validación", "🧮 Cálculo", "📈 Resultados", "📄 Reportes"
])

# ===== TAB 1: DATOS =====
with tab1:
    st.header("📊 Vista de Datos Cargados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Factores de Emisión")
        if st.session_state.factors_df is not None:
            st.success(f"✅ {len(st.session_state.factors_df)} factores disponibles")
            
            # Filtros para explorar factores
            if 'Sheet' in st.session_state.factors_df.columns:
                selected_sheet = st.selectbox(
                    "Filtrar por hoja",
                    ["Todas"] + list(st.session_state.factors_df['Sheet'].unique())
                )
                if selected_sheet != "Todas":
                    display_factors = st.session_state.factors_df[
                        st.session_state.factors_df['Sheet'] == selected_sheet
                    ]
                else:
                    display_factors = st.session_state.factors_df
            else:
                display_factors = st.session_state.factors_df
            
            st.dataframe(
                display_factors.head(50),
                use_container_width=True,
                height=400
            )
        else:
            st.info("ℹ️ Carga un archivo de factores de emisión en la barra lateral")
    
    with col2:
        st.subheader("Datos de Actividad")
        if st.session_state.activity_df is not None:
            st.success(f"✅ {len(st.session_state.activity_df)} actividades cargadas")
            
            # Resumen rápido
            summary = get_data_quality_summary(st.session_state.activity_df)
            
            col2a, col2b, col2c = st.columns(3)
            col2a.metric("Filas", summary['total_rows'])
            col2b.metric("Columnas", summary['total_columns'])
            col2c.metric("Duplicados", summary['duplicate_rows'])
            
            st.dataframe(
                st.session_state.activity_df,
                use_container_width=True,
                height=400
            )
            
            # Mostrar estadísticas por scope
            if 'scope' in st.session_state.activity_df.columns:
                st.subheader("Distribución por Scope")
                scope_dist = st.session_state.activity_df['scope'].value_counts().sort_index()
                fig_scope = px.bar(
                    x=scope_dist.index,
                    y=scope_dist.values,
                    labels={'x': 'Scope', 'y': 'Cantidad'},
                    title="Actividades por Alcance",
                    color=scope_dist.index,
                    color_discrete_map={1: '#FF6B6B', 2: '#4ECDC4', 3: '#45B7D1'}
                )
                st.plotly_chart(fig_scope, use_container_width=True)
        else:
            st.info("ℹ️ Carga un archivo de datos de actividad en la barra lateral")
    
    # 🆕 ASISTENTE IA - Categorización Automática
    st.markdown("---")
    st.subheader("🤖 Asistente IA - Categorización Automática")
    
    with st.expander("💡 ¿Cómo funciona?", expanded=False):
        st.markdown("""
        El **Asistente IA** usa inteligencia artificial local (Ollama) para categorizar
        automáticamente actividades en lenguaje natural según el GHG Protocol.
        
        **Ejemplos de uso:**
        - 📝 "consumo de diesel en tractores" → Scope 1: mobile_combustion
        - 📝 "electricidad de la red" → Scope 2: purchased_electricity  
        - 📝 "vuelos de negoc ios" → Scope 3: business_travel
        
        **Ventajas:**
        - ✅ 100% local y gratuito (usa Ollama)
        - ✅ Sin APIs de pago
        - ✅ Privacidad garantizada (datos no salen de tu PC)
        - ✅ Funciona offline
        - ✅ Fallback inteligente si Ollama no está disponible
        """)
    
    col_ai1, col_ai2 = st.columns([2, 1])
    
    with col_ai1:
        activity_description = st.text_input(
            "Describe tu actividad en lenguaje natural:",
            placeholder="Ej: consumo de gas natural en calderas industriales",
            help="El asistente identificará automáticamente el Scope y categoría"
        )
    
    with col_ai2:
        st.markdown("<br>", unsafe_allow_html=True)  # Espaciado
        categorize_button = st.button("🔮 Categorizar", type="primary", use_container_width=True)
    
    if categorize_button and activity_description:
        with st.spinner("🤖 Analizando con IA..."):
            try:
                from utils.ai_assistant import GHGCategoryMapper, check_ollama_status
                
                # Verificar estado de Ollama
                status = check_ollama_status()
                
                if not status['running']:
                    st.warning("⚠️ Ollama no está corriendo. Usando categorización basada en reglas...")
                
                # Categorizar
                mapper = GHGCategoryMapper()
                result = mapper.map_activity(activity_description)
                
                # Mostrar resultados
                st.success("✅ Categorización completada!")
                
                col_res1, col_res2, col_res3 = st.columns(3)
                
                with col_res1:
                    st.metric(
                        "Scope",
                        result.scope,
                        help=f"Alcance GHG Protocol"
                    )
                
                with col_res2:
                    st.metric(
                        "Categoría",
                        result.category.replace('_', ' ').title(),
                        help="Categoría específica"
                    )
                
                with col_res3:
                    confidence_color = "🟢" if result.confidence >= 0.8 else "🟡" if result.confidence >= 0.6 else "🔴"
                    st.metric(
                        "Confianza",
                        f"{result.confidence:.0%}",
                        delta=confidence_color,
                        help="Nivel de certeza del modelo"
                    )
                
                # Explicación
                st.info(f"💡 **Explicación**: {result.explanation}")
                
                # Combustible identificado
                if result.fuel_type:
                    st.success(f"⛽ **Combustible detectado**: {result.fuel_type}")
                
                # Sugerencias
                if result.suggestions:
                    with st.expander("📋 Sugerencias para mejorar la precisión"):
                        for sug in result.suggestions:
                            st.write(f"- {sug}")
                
                # Código para usar
                with st.expander("💻 Código para agregar a tu CSV"):
                    code_example = f"""entity_id,scope,category,activity_value,activity_unit,geography,year
mi_entidad,{result.scope},{result.category},100,liters,GBR,2024"""
                    st.code(code_example, language="csv")
                
            except ImportError as e:
                st.error(f"❌ Error al importar módulo de IA: {e}")
                st.info("Asegúrate de que `utils/ai_assistant.py` existe")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("Verifica que Ollama esté instalado: https://ollama.com/download")
    
    # Sección de búsqueda semántica de factores
    st.markdown("---")
    st.subheader("🔎 Búsqueda Semántica de Factores de Emisión")
    
    with st.expander("💡 ¿Qué es la búsqueda semántica?"):
        st.markdown("""
        La búsqueda semántica te ayuda a **encontrar los factores de emisión exactos** 
        para tu actividad sin necesidad de conocer la nomenclatura técnica.
        
        **Cómo funciona:**
        1. 🔍 Describes tu actividad en lenguaje natural
        2. 🤖 El sistema categoriza automáticamente (Scope + categoría)
        3. 📊 Busca los factores más relevantes en la base de datos UK Gov 2025
        4. ✅ Te muestra el valor exacto de kg CO2e por unidad
        
        **Ejemplos:**
        - 📝 "diesel en camiones" → 2.57082 kg CO2e/litro
        - 📝 "gas natural para calefacción" → 0.2027 kg CO2e/kWh
        - 📝 "vuelo corto doméstico" → kg CO2e/pasajero-km
        
        **Ventajas:**
        - ✅ Búsqueda multi-nivel (exacta, sinónimos, fuzzy)
        - ✅ Cache de resultados para velocidad
        - ✅ 521 factores de emisión UK Gov 2025
        - ✅ Scoring de relevancia (0-100%)
        """)
    
    col_search1, col_search2 = st.columns([2, 1])
    
    with col_search1:
        search_query = st.text_input(
            "Busca un factor de emisión:",
            placeholder="Ej: diesel en camiones de distribución",
            help="Describe la actividad para encontrar el factor exacto",
            key="semantic_search_input"
        )
    
    with col_search2:
        st.markdown("<br>", unsafe_allow_html=True)
        search_button = st.button("🔍 Buscar Factor", type="secondary", use_container_width=True)
    
    if search_button and search_query:
        with st.spinner("🔎 Buscando factores relevantes..."):
            try:
                from utils.ai_assistant import SemanticFactorSearch
                from utils.factors import load_uk_gov_factors
                
                # Cargar factores (con cache de Streamlit)
                @st.cache_data
                def get_factors():
                    factors_path = 'data/ghg-conversion-factors-2025-condensed-set.xlsx'
                    return load_uk_gov_factors(factors_path, year=2025)
                
                factors_df = get_factors()
                
                # Buscar con categorización automática
                searcher = SemanticFactorSearch(factors_df)
                results = searcher.search_with_category(search_query, top_k=5)
                
                if results:
                    st.success(f"✅ Encontrados {len(results)} factores relevantes!")
                    
                    # Mostrar resultados en tabla
                    results_data = []
                    for i, match in enumerate(results, 1):
                        results_data.append({
                            "#": i,
                            "Factor": match.factor_name,
                            "Valor": f"{match.value:.5f}",
                            "Unidad": match.unit,
                            "Categoría": match.category,
                            "Relevancia": f"{match.match_score:.0%}"
                        })
                    
                    st.dataframe(
                        pd.DataFrame(results_data),
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    # Mejor match destacado
                    best_match = results[0]
                    st.info(f"""
**🎯 Mejor Match**: {best_match.factor_name}

- 📊 **Factor de emisión**: `{best_match.value:.5f} kg CO2e / {best_match.unit}`
- 🔢 **Relevancia**: {best_match.match_score:.0%}
- 📁 **Categoría**: {best_match.category}
- 🌍 **Geografía**: {best_match.geography}
- 📅 **Año**: {best_match.year}

**💻 Código para tu CSV:**
```csv
entity_id,scope,category,activity_value,activity_unit,ghg_factor,geography,year
mi_entidad,1,mobile_combustion,1000,{best_match.unit},{best_match.value},{best_match.geography},{best_match.year}
```
                    """)
                    
                else:
                    st.warning("⚠️ No se encontraron factores relevantes para esta búsqueda.")
                    st.info("💡 Intenta con términos más generales como 'diesel', 'electricidad', 'vuelo', etc.")
                
            except Exception as e:
                st.error(f"❌ Error en búsqueda: {str(e)}")
                import traceback
                st.code(traceback.format_exc())

# ===== TAB 2: VALIDACIÓN =====
with tab2:
    st.header("🔍 Validación de Datos")
    
    if st.session_state.activity_df is not None:
        if st.button("🔍 Validar Datos", type="primary"):
            with st.spinner("Validando datos..."):
                valid_activities, report = validate_activity_data(
                    st.session_state.activity_df,
                    strict=strict_validation
                )
                st.session_state.valid_activities = valid_activities
                st.session_state.validation_report = report
        
        if st.session_state.validation_report:
            report = st.session_state.validation_report
            
            # Métricas de validación
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Filas", report.total_rows)
            col2.metric("Filas Válidas", report.valid_rows, delta=f"{report.success_rate:.1f}%")
            col3.metric("Filas Inválidas", report.invalid_rows)
            col4.metric("Errores", len(report.errors))
            
            # Resultado de validación
            if report.success_rate >= 80:
                st.markdown(
                    f'<div class="success-box">✅ Validación exitosa: {report.success_rate:.1f}% de datos válidos</div>',
                    unsafe_allow_html=True
                )
            elif report.success_rate >= 50:
                st.markdown(
                    f'<div class="warning-box">⚠️ Validación con advertencias: {report.success_rate:.1f}% de datos válidos</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div class="error-box">❌ Validación fallida: {report.success_rate:.1f}% de datos válidos</div>',
                    unsafe_allow_html=True
                )
            
            # Mostrar errores si existen
            if report.errors:
                st.subheader("❌ Errores Detectados")
                errors_df = report.to_dataframe()
                st.dataframe(errors_df, use_container_width=True)
                
                # Descarga de reporte de errores
                csv_errors = errors_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "⬇️ Descargar Reporte de Errores (CSV)",
                    csv_errors,
                    "errores_validacion.csv",
                    "text/csv"
                )
            
            # Advertencias
            if report.warnings:
                st.subheader("⚠️ Advertencias")
                for warning in report.warnings:
                    st.warning(warning)
    else:
        st.info("ℹ️ Carga datos de actividad primero")

# ===== TAB 3: CÁLCULO =====
with tab3:
    st.header("🧮 Cálculo de Emisiones")
    
    can_calculate = (
        st.session_state.factors_df is not None and
        len(st.session_state.valid_activities) > 0
    )
    
    if can_calculate:
        st.success(f"✅ Listo para calcular: {len(st.session_state.valid_activities)} actividades válidas")
        
        if st.button("🚀 Calcular Huella de Carbono", type="primary", use_container_width=True):
            with st.spinner("Calculando emisiones... Por favor espera."):
                results = []
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                total_activities = len(st.session_state.valid_activities)
                
                for idx, activity in enumerate(st.session_state.valid_activities):
                    try:
                        # Actualizar progreso
                        progress = (idx + 1) / total_activities
                        progress_bar.progress(progress)
                        status_text.text(
                            f"Procesando {idx + 1}/{total_activities}: "
                            f"{activity.entity_id} - Scope {activity.scope}"
                        )
                        
                        # Buscar factor
                        factor_result = find_factor(
                            st.session_state.factors_df,
                            activity.category,
                            activity.activity_unit,
                            geography=activity.geography,
                            scope=activity.scope
                        )
                        
                        if factor_result:
                            factor_value, factor_source, metadata = factor_result
                            
                            # Crear EmissionFactor
                            ef = EmissionFactor(
                                source="UK2025",
                                gas="CO2e",
                                value=factor_value,
                                unit=metadata['unit'],
                                year=metadata['year'],
                                geography=metadata.get('geography'),
                                scope=activity.scope,
                                category=activity.category,
                                notes=metadata.get('full_description')
                            )
                            
                            # Calcular emisión
                            result = compute_emission(
                                activity,
                                ef,
                                auto_convert_units=auto_unit_conversion
                            )
                            results.append(result)
                        
                        else:
                            logger.warning(
                                f"No factor found for {activity.entity_id} - "
                                f"{activity.category} ({activity.activity_unit})"
                            )
                    
                    except Exception as e:
                        logger.error(f"Error calculating {activity.entity_id}: {e}")
                        continue
                
                progress_bar.empty()
                status_text.empty()
                
                st.session_state.results = results
                
                if results:
                    st.success(f"✅ Cálculo completado: {len(results)} emisiones calculadas")
                else:
                    st.error("❌ No se pudieron calcular emisiones. Revisa los factores y datos.")
    
    elif st.session_state.activity_df is not None:
        st.warning("⚠️ Valida los datos primero en la pestaña 'Validación'")
    elif st.session_state.factors_df is None:
        st.warning("⚠️ Carga factores de emisión primero")
    else:
        st.info("ℹ️ Carga datos de actividad y factores de emisión para comenzar")

# ===== TAB 4: RESULTADOS =====
with tab4:
    st.header("📈 Resultados de Huella de Carbono")
    
    if st.session_state.results:
        results = st.session_state.results
        
        # Totales generales
        totals = get_total_emissions(results)
        
        st.subheader("🌍 Huella de Carbono Total")
        col1, col2, col3 = st.columns(3)
        col1.metric(
            "Total Emisiones",
            f"{totals['total_tonnes_co2e']:.2f} tCO₂e",
            help="Toneladas de CO₂ equivalente"
        )
        col2.metric(
            "Actividades Calculadas",
            totals['count_activities']
        )
        col3.metric(
            "kg CO₂e",
            f"{totals['total_kg_co2e']:,.0f}"
        )
        
        st.markdown("---")
        
        # Agregaciones
        scope_agg = aggregate_emissions_by_scope(results)
        category_agg = aggregate_emissions_by_category(results)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Emisiones por Alcance (Scope)")
            
            scope_df = pd.DataFrame([
                {'Scope': f'Scope {k}', 'tCO2e': v, 'Porcentaje': v/totals['total_tonnes_co2e']*100}
                for k, v in scope_agg.items() if v > 0
            ])
            
            if not scope_df.empty:
                fig_scope_pie = px.pie(
                    scope_df,
                    values='tCO2e',
                    names='Scope',
                    title='Distribución por Alcance GHG Protocol',
                    color='Scope',
                    color_discrete_map={
                        'Scope 1': '#FF6B6B',
                        'Scope 2': '#4ECDC4',
                        'Scope 3': '#45B7D1'
                    }
                )
                st.plotly_chart(fig_scope_pie, use_container_width=True)
                
                st.dataframe(
                    scope_df.style.format({'tCO2e': '{:.2f}', 'Porcentaje': '{:.1f}%'}),
                    use_container_width=True
                )
        
        with col2:
            st.subheader("📊 Top 10 Categorías")
            
            category_df = pd.DataFrame([
                {'Categoría': k, 'tCO2e': v}
                for k, v in sorted(category_agg.items(), key=lambda x: x[1], reverse=True)[:10]
            ])
            
            if not category_df.empty:
                fig_cat = px.bar(
                    category_df,
                    x='tCO2e',
                    y='Categoría',
                    orientation='h',
                    title='Emisiones por Categoría',
                    color='tCO2e',
                    color_continuous_scale='Greens'
                )
                st.plotly_chart(fig_cat, use_container_width=True)
        
        # 🆕 QUICK WIN #1: Sankey Diagram - Flujo de emisiones (CON CACHE)
        st.subheader("🌊 Flujo de Emisiones (Diagrama Sankey)")
        
        # Usar versión cacheada para mejorar rendimiento
        with st.expander("📊 Ver Diagrama Sankey", expanded=False):
            try:
                fig_sankey = create_sankey_chart(tuple(results))  # tuple para hashable
                
                if fig_sankey:
                    st.plotly_chart(fig_sankey, use_container_width=True)
                    st.info("💡 El diagrama Sankey muestra el flujo de emisiones desde los Scopes (1, 2, 3) hacia las categorías específicas y finalmente hacia las entidades. El grosor de cada flujo representa la magnitud de las emisiones.")
                else:
                    st.info("📊 No hay suficientes datos para generar el diagrama Sankey.")
            except Exception as e:
                st.error(f"Error generando Sankey: {e}")
                logger.error(f"Sankey generation error: {e}")
        
        # 🆕 QUICK WIN #2: Treemap Interactivo - Jerarquía de emisiones (CON CACHE)
        st.subheader("🗺️ Mapa Jerárquico de Emisiones (Treemap)")
        
        # Usar versión cacheada para mejorar rendimiento
        with st.expander("🗺️ Ver Treemap Jerárquico", expanded=False):
            try:
                fig_treemap = create_treemap_chart(tuple(results))  # tuple para hashable
                
                if fig_treemap:
                    st.plotly_chart(fig_treemap, use_container_width=True)
                    st.info("💡 Haz clic en cualquier recuadro para hacer zoom y explorar en detalle. El tamaño representa las emisiones totales, el color indica la intensidad relativa.")
                else:
                    st.info("📊 No hay datos para el mapa jerárquico.")
            except Exception as e:
                st.error(f"Error generando Treemap: {e}")
                logger.error(f"Treemap generation error: {e}")
        
        # 🆕 QUICK WIN #3: Comparación Temporal
        st.subheader("📅 Evolución Temporal de Emisiones")
        
        # Extraer información temporal de actividades
        temporal_data = []
        for r in results:
            activity = r.activity_record
            # Intentar obtener year/month del activity_record
            year = getattr(activity, 'year', None) or getattr(activity, 'fiscal_year', 2024)
            month = getattr(activity, 'month', None)
            
            if month:
                period = f"{year}-{month:02d}"
            else:
                period = str(year)
            
            temporal_data.append({
                'Periodo': period,
                'Scope': f'Scope {activity.scope}',
                'Categoría': r.category_label,
                'Emisión (tCO2e)': r.emission_tCO2e
            })
        
        if temporal_data:
            temporal_df = pd.DataFrame(temporal_data)
            
            # Agrupar por periodo y scope
            period_scope = temporal_df.groupby(['Periodo', 'Scope'])['Emisión (tCO2e)'].sum().reset_index()
            
            if len(period_scope['Periodo'].unique()) > 1:
                # Gráfico de líneas si hay múltiples periodos
                fig_temporal = px.line(
                    period_scope,
                    x='Periodo',
                    y='Emisión (tCO2e)',
                    color='Scope',
                    markers=True,
                    title='Evolución de Emisiones por Scope',
                    labels={'Emisión (tCO2e)': 'Emisiones (tCO2e)', 'Periodo': 'Periodo'},
                    color_discrete_map={
                        'Scope 1': '#FF6B6B',
                        'Scope 2': '#4ECDC4',
                        'Scope 3': '#95E1D3'
                    }
                )
                
                fig_temporal.update_layout(
                    height=400,
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig_temporal, use_container_width=True)
                
                # Análisis de tendencia
                total_by_period = temporal_df.groupby('Periodo')['Emisión (tCO2e)'].sum().reset_index()
                if len(total_by_period) >= 2:
                    first_value = total_by_period.iloc[0]['Emisión (tCO2e)']
                    last_value = total_by_period.iloc[-1]['Emisión (tCO2e)']
                    change = ((last_value - first_value) / first_value) * 100
                    
                    col_trend1, col_trend2, col_trend3 = st.columns(3)
                    
                    with col_trend1:
                        st.metric(
                            "Primer Periodo",
                            f"{first_value:.2f} tCO2e",
                            delta=None
                        )
                    
                    with col_trend2:
                        st.metric(
                            "Último Periodo",
                            f"{last_value:.2f} tCO2e",
                            delta=f"{change:+.1f}%"
                        )
                    
                    with col_trend3:
                        direction = "📈 Aumento" if change > 0 else "📉 Reducción"
                        st.metric(
                            "Tendencia",
                            direction,
                            delta=f"{abs(change):.1f}%"
                        )
                
                st.info("💡 **Análisis Temporal**: Este gráfico muestra la evolución de tus emisiones a lo largo del tiempo. Si hay múltiples meses, puedes identificar tendencias y patrones estacionales.")
            else:
                st.info("📊 Solo hay datos de un periodo. Carga actividades de varios meses/años para ver la evolución temporal.")
        
        # 🆕 RECOMENDACIONES IA
        st.markdown("---")
        st.subheader("💡 Recomendaciones Inteligentes para Reducir Emisiones")
        
        with st.expander("🤖 ¿Cómo funciona el motor de recomendaciones?", expanded=False):
            st.markdown("""
            El motor de recomendaciones **analiza tu huella de carbono** y genera sugerencias priorizadas:
            
            **Análisis realizado:**
            - 📊 **Distribución por Scope** (1, 2, 3) - Identifica hotspots
            - 📁 **Top categorías** - Encuentra las 3 fuentes principales
            - 🌍 **Comparación sectorial** - Compara con benchmarks de tu industria
            - 🎯 **Priorización** - Ordena por impacto potencial
            
            **Resultados:**
            - ✅ Recomendaciones priorizadas (Alta, Media, Baja)
            - ✅ Estimación de % de reducción potencial
            - ✅ Dificultad de implementación (Fácil, Media, Difícil)
            - ✅ Plazo estimado (Corto, Mediano, Largo)
            - ✅ Costo aproximado ($, $$, $$$)
            - ✅ Acciones específicas paso a paso
            
            **100% local y gratuito** - Sin APIs de pago
            """)
        
        # Inputs para recomendaciones
        col_rec1, col_rec2 = st.columns(2)
        
        with col_rec1:
            sector_input = st.selectbox(
                "Sector de tu empresa:",
                options=[
                    ("default", "General / No especificado"),
                    ("services", "Servicios / Oficinas"),
                    ("manufacturing", "Manufactura / Industrial"),
                    ("transport", "Transporte / Logística"),
                    ("retail", "Retail / Comercio"),
                    ("technology", "Tecnología / IT")
                ],
                format_func=lambda x: x[1],
                help="El benchmark varía según el sector"
            )
            sector_value = sector_input[0]
        
        with col_rec2:
            num_employees_input = st.number_input(
                "Número de empleados (opcional):",
                min_value=1,
                max_value=100000,
                value=None,
                help="Para comparar con benchmark sectorial (kg CO2e/empleado/año)"
            )
        
        if st.button("🔮 Generar Recomendaciones", type="primary", use_container_width=True):
            with st.spinner("🤖 Analizando tu huella de carbono..."):
                try:
                    from utils.ai_recommendations import AIRecommendationEngine
                    
                    # Preparar datos
                    emissions_by_scope = {
                        scope: total for scope, total in scope_agg.items() if total > 0
                    }
                    
                    emissions_by_category = {
                        cat: total for cat, total in category_agg.items() if total > 0
                    }
                    
                    total_emissions_kg = totals['total_kg_co2e']
                    
                    # Generar recomendaciones
                    engine = AIRecommendationEngine()
                    recommendations = engine.analyze_and_recommend(
                        emissions_by_scope=emissions_by_scope,
                        emissions_by_category=emissions_by_category,
                        total_emissions=total_emissions_kg,
                        sector=sector_value,
                        num_employees=num_employees_input
                    )
                    
                    # Guardar en session_state
                    st.session_state.recommendations = recommendations
                    
                    st.success(f"✅ Generadas {len(recommendations)} recomendaciones!")
                    
                except ImportError as e:
                    st.error(f"❌ Error al importar módulo de recomendaciones: {e}")
                    st.info("Asegúrate de que `utils/ai_recommendations.py` existe")
                except Exception as e:
                    st.error(f"❌ Error generando recomendaciones: {str(e)}")
                    import traceback
                    st.code(traceback.format_exc())
        
        # Mostrar recomendaciones si existen
        if 'recommendations' in st.session_state and st.session_state.recommendations:
            recs = st.session_state.recommendations
            
            # Resumen ejecutivo
            st.markdown("---")
            st.subheader("📊 Resumen de Recomendaciones")
            
            high_priority = [r for r in recs if r.priority == 1]
            total_reduction = sum(r.estimated_reduction_pct for r in recs)
            
            col_sum1, col_sum2, col_sum3 = st.columns(3)
            
            with col_sum1:
                st.metric(
                    "Total Recomendaciones",
                    len(recs),
                    help="Número total de recomendaciones generadas"
                )
            
            with col_sum2:
                st.metric(
                    "Prioridad Alta",
                    len(high_priority),
                    help="Recomendaciones de mayor impacto"
                )
            
            with col_sum3:
                st.metric(
                    "Reducción Potencial",
                    f"{total_reduction:.1f}%",
                    help="Suma de todas las reducciones potenciales"
                )
            
            # Top 3 Recomendaciones Prioritarias
            st.markdown("---")
            st.subheader("🔥 Top 3 Recomendaciones (Mayor Impacto)")
            
            top_3 = sorted(recs, key=lambda x: (x.priority, -x.estimated_reduction_pct))[:3]
            
            for i, rec in enumerate(top_3, 1):
                # Color según prioridad
                priority_color = {
                    1: "🔴",
                    2: "🟡",
                    3: "🟢"
                }
                
                with st.container():
                    st.markdown(f"### {priority_color[rec.priority]} {i}. {rec.title}")
                    
                    col_rec_info1, col_rec_info2, col_rec_info3, col_rec_info4 = st.columns(4)
                    
                    with col_rec_info1:
                        st.metric("Categoría", rec.category)
                    
                    with col_rec_info2:
                        impact_emoji = {"Alto": "🚀", "Medio": "📊", "Bajo": "📉"}
                        st.metric("Impacto", f"{impact_emoji.get(rec.impact_potential, '')} {rec.impact_potential}")
                    
                    with col_rec_info3:
                        st.metric("Reducción", f"{rec.estimated_reduction_pct:.1f}%")
                    
                    with col_rec_info4:
                        st.metric("Plazo", rec.timeframe.split()[0])
                    
                    st.info(f"**📝 Descripción**: {rec.description}")
                    
                    st.markdown(f"**⚙️ Dificultad**: {rec.implementation_difficulty} | **💰 Costo**: {rec.cost_range}")
                    
                    st.markdown("**✅ Acciones recomendadas:**")
                    for action in rec.actions:
                        st.markdown(f"- {action}")
                    
                    st.markdown("---")
            
            # Todas las recomendaciones por prioridad
            with st.expander("📋 Ver todas las recomendaciones", expanded=False):
                for priority_level in [1, 2, 3]:
                    priority_recs = [r for r in recs if r.priority == priority_level]
                    
                    if not priority_recs:
                        continue
                    
                    priority_labels = {1: "Alta 🔴", 2: "Media 🟡", 3: "Baja 🟢"}
                    st.markdown(f"### Prioridad {priority_labels[priority_level]}")
                    
                    for rec in priority_recs:
                        st.markdown(f"**{rec.title}** ({rec.category})")
                        st.markdown(f"- Reducción: {rec.estimated_reduction_pct:.1f}% | Impacto: {rec.impact_potential} | Dificultad: {rec.implementation_difficulty}")
                        st.markdown(f"- Plazo: {rec.timeframe} | Costo: {rec.cost_range}")
                        st.markdown("")
            
            # Descargar reporte de recomendaciones
            st.markdown("---")
            st.subheader("⬇️ Descargar Reporte de Recomendaciones")
            
            # Generar reporte
            report_md = engine.generate_summary_report(recs)
            
            col_dl_rec1, col_dl_rec2 = st.columns(2)
            
            with col_dl_rec1:
                st.download_button(
                    "📥 Descargar Reporte (Markdown)",
                    report_md.encode('utf-8'),
                    f"recomendaciones_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    "text/markdown",
                    use_container_width=True
                )
            
            with col_dl_rec2:
                # Convertir a CSV simple
                recs_csv_data = []
                for rec in recs:
                    recs_csv_data.append({
                        'Prioridad': rec.priority,
                        'Título': rec.title,
                        'Categoría': rec.category,
                        'Impacto': rec.impact_potential,
                        'Reducción %': rec.estimated_reduction_pct,
                        'Dificultad': rec.implementation_difficulty,
                        'Plazo': rec.timeframe,
                        'Costo': rec.cost_range,
                        'Acciones': '; '.join(rec.actions)
                    })
                
                recs_csv = pd.DataFrame(recs_csv_data).to_csv(index=False).encode('utf-8')
                
                st.download_button(
                    "📥 Descargar Reporte (CSV)",
                    recs_csv,
                    f"recomendaciones_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    "text/csv",
                    use_container_width=True
                )
        
        # Tabla detallada de resultados
        st.subheader("📋 Detalle de Resultados")
        
        results_data = []
        for r in results:
            results_data.append({
                'Entidad': r.activity_record.entity_id,
                'Scope': r.activity_record.scope,
                'Categoría': r.category_label,
                'Actividad': f"{r.activity_record.activity_value} {r.activity_record.activity_unit}",
                'Factor (kg CO₂e)': r.emission_factor.value,
                'Emisión (kg CO₂e)': r.emission_kgCO2e,
                'Emisión (tCO₂e)': r.emission_tCO2e,
                'Fuente Factor': r.emission_factor.source,
                'Año': r.emission_factor.year
            })
        
        results_df = pd.DataFrame(results_data)
        st.dataframe(results_df, use_container_width=True, height=400)
        
        # Descargas
        st.subheader("⬇️ Descargar Resultados")
        
        # Verificar dependencias
        deps = check_dependencies()
        
        col_down1, col_down2, col_down3, col_down4 = st.columns(4)
        
        with col_down1:
            csv_results = results_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 CSV",
                csv_results,
                f"huella_carbono_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                "text/csv",
                use_container_width=True
            )
        
        with col_down2:
            # Resumen ejecutivo
            summary_text = f"""RESUMEN EJECUTIVO - HUELLA DE CARBONO
Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Metodología: GHG Protocol

TOTALES:
- Emisiones Totales: {totals['total_tonnes_co2e']:.2f} tCO₂e
- Actividades Calculadas: {totals['count_activities']}

POR ALCANCE:
- Scope 1: {scope_agg[1]:.2f} tCO₂e ({scope_agg[1]/totals['total_tonnes_co2e']*100:.1f}%)
- Scope 2: {scope_agg[2]:.2f} tCO₂e ({scope_agg[2]/totals['total_tonnes_co2e']*100:.1f}%)
- Scope 3: {scope_agg[3]:.2f} tCO₂e ({scope_agg[3]/totals['total_tonnes_co2e']*100:.1f}%)

Fuente de Factores: {factor_source}
"""
            st.download_button(
                "📄 TXT",
                summary_text,
                f"resumen_{datetime.now().strftime('%Y%m%d')}.txt",
                "text/plain",
                use_container_width=True
            )
        
        with col_down3:
            if deps['excel']:
                try:
                    metadata = {
                        'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'factor_source': factor_source,
                        'actividades': totals['count_activities']
                    }
                    excel_file = generate_excel_report(
                        results_df, scope_agg, category_agg,
                        totals['total_tonnes_co2e'], metadata
                    )
                    st.download_button(
                        "� Excel",
                        excel_file,
                        f"reporte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"Error generando Excel: {e}")
            else:
                st.button("📊 Excel", disabled=True, use_container_width=True,
                         help="Instale openpyxl: pip install openpyxl")
        
        with col_down4:
            if deps['word']:
                try:
                    metadata = {
                        'fecha': datetime.now().strftime('%Y-%m-%d'),
                        'factor_source': factor_source,
                        'actividades': totals['count_activities']
                    }
                    word_file = generate_word_report(
                        results_df, scope_agg, category_agg,
                        totals['total_tonnes_co2e'], metadata
                    )
                    st.download_button(
                        "📝 Word",
                        word_file,
                        f"reporte_APA7_{datetime.now().strftime('%Y%m%d')}.docx",
                        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"Error generando Word: {e}")
            else:
                st.button("📝 Word", disabled=True, use_container_width=True,
                         help="Instale python-docx: pip install python-docx")
    
    else:
        st.info("ℹ️ Calcula las emisiones primero en la pestaña 'Cálculo'")

# ===== TAB 5: REPORTES =====
with tab5:
    st.header("📄 Generación de Reportes")
    
    st.info("🚧 Módulo de reportes en formato APA 7 - Próximamente")
    
    st.markdown("""
    ### Funcionalidades Planificadas:
    
    - 📝 **Reporte PDF**: Formato APA 7ª edición con:
      - Portada
      - Resumen ejecutivo
      - Metodología (GHG Protocol)
      - Resultados por alcance y categoría
      - Gráficos y tablas
      - Supuestos y limitaciones
      - Referencias bibliográficas
    
    - 📊 **Dashboard Interactivo**: Visualizaciones avanzadas con Plotly
    - 🔄 **Reporte Comparativo**: Comparar múltiples periodos
    - 🎯 **Recomendaciones**: Sugerencias de reducción de emisiones
    """)

# ===== FOOTER =====
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem 0;'>
    <p><strong>Calculadora de Huella de Carbono v1.0</strong></p>
    <p>Basado en GHG Protocol | IPCC Guidelines | UK Gov Factors</p>
    <p>© 2025 | Desarrollado con Python + Streamlit</p>
</div>
""", unsafe_allow_html=True)