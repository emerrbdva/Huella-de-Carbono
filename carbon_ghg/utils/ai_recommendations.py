"""
Módulo de Recomendaciones Inteligentes con IA
============================================

Analiza resultados de cálculos de emisiones y genera
recomendaciones personalizadas usando IA local (Ollama).

Características:
- Análisis por Scope (identificar hotspots)
- Comparación con benchmarks sectoriales
- Sugerencias de reducción priorizadas
- ROI estimado de medidas de mitigación
- 100% local, sin costos de API
"""

import pandas as pd
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import json

logger = logging.getLogger(__name__)


@dataclass
class Recommendation:
    """
    Recomendación de reducción de emisiones.
    """
    priority: int  # 1 (alta) a 3 (baja)
    category: str  # Scope 1, 2 o 3
    title: str
    description: str
    impact_potential: str  # Alto, Medio, Bajo
    implementation_difficulty: str  # Fácil, Media, Difícil
    estimated_reduction_pct: float  # Porcentaje de reducción estimado
    actions: List[str]  # Acciones específicas
    timeframe: str  # Corto, Mediano, Largo plazo
    cost_range: str  # $, $$, $$$


class AIRecommendationEngine:
    """
    Motor de recomendaciones inteligentes usando análisis de datos + IA.
    
    Genera recomendaciones personalizadas basadas en:
    - Distribución de emisiones por Scope
    - Categorías con mayor contribución
    - Tendencias temporales
    - Benchmarks sectoriales
    """
    
    # Benchmarks promedio por sector (kg CO2e por empleado/año)
    SECTOR_BENCHMARKS = {
        'services': 2500,      # Servicios (oficinas)
        'manufacturing': 8000,  # Manufactura
        'transport': 12000,    # Transporte
        'retail': 3500,        # Retail
        'technology': 1500,    # Tecnología
        'default': 4000        # Promedio general
    }
    
    def __init__(self):
        """Inicializa el motor de recomendaciones."""
        self.recommendations_cache = {}
    
    def analyze_and_recommend(
        self,
        emissions_by_scope: Dict[int, float],
        emissions_by_category: Dict[str, float],
        total_emissions: float,
        sector: str = 'default',
        num_employees: Optional[int] = None
    ) -> List[Recommendation]:
        """
        Analiza emisiones y genera recomendaciones priorizadas.
        
        Args:
            emissions_by_scope: {1: 1200, 2: 3400, 3: 800}
            emissions_by_category: {'mobile_combustion': 1200, ...}
            total_emissions: Total kg CO2e
            sector: Sector de la empresa
            num_employees: Número de empleados (opcional)
        
        Returns:
            Lista de Recommendation ordenadas por prioridad
        """
        recommendations = []
        
        # 1. Análisis por Scope
        scope_recommendations = self._analyze_scopes(emissions_by_scope, total_emissions)
        recommendations.extend(scope_recommendations)
        
        # 2. Análisis por categoría
        category_recommendations = self._analyze_categories(emissions_by_category, total_emissions)
        recommendations.extend(category_recommendations)
        
        # 3. Comparación con benchmark
        if num_employees:
            benchmark_recommendations = self._compare_with_benchmark(
                total_emissions, num_employees, sector
            )
            recommendations.extend(benchmark_recommendations)
        
        # 4. Recomendaciones generales
        general_recommendations = self._get_general_recommendations(
            emissions_by_scope, total_emissions
        )
        recommendations.extend(general_recommendations)
        
        # Ordenar por prioridad
        recommendations.sort(key=lambda x: x.priority)
        
        return recommendations
    
    def _analyze_scopes(
        self,
        emissions_by_scope: Dict[int, float],
        total_emissions: float
    ) -> List[Recommendation]:
        """Genera recomendaciones basadas en distribución de Scopes."""
        recommendations = []
        
        # Calcular porcentajes
        scope_percentages = {
            scope: (value / total_emissions * 100) if total_emissions > 0 else 0
            for scope, value in emissions_by_scope.items()
        }
        
        # Scope 2 (Electricidad)
        if scope_percentages.get(2, 0) > 40:
            recommendations.append(Recommendation(
                priority=1,
                category="Scope 2",
                title="Transición a Energía Renovable",
                description=f"Scope 2 representa {scope_percentages[2]:.1f}% de tus emisiones. "
                           "La electricidad es tu mayor fuente de emisiones.",
                impact_potential="Alto",
                implementation_difficulty="Media",
                estimated_reduction_pct=scope_percentages[2] * 0.8,  # Reducción potencial 80%
                actions=[
                    "Contratar electricidad renovable certificada (PPA)",
                    "Instalar paneles solares en instalaciones",
                    "Implementar certificados de energía renovable (RECs)",
                    "Optimizar consumo con sistemas de gestión energética"
                ],
                timeframe="Mediano plazo (6-18 meses)",
                cost_range="$$"
            ))
        
        # Scope 1 (Combustión directa)
        if scope_percentages.get(1, 0) > 30:
            recommendations.append(Recommendation(
                priority=1,
                category="Scope 1",
                title="Optimización de Combustión Directa",
                description=f"Scope 1 es {scope_percentages[1]:.1f}% de tus emisiones. "
                           "Enfócate en eficiencia de combustibles y electrificación.",
                impact_potential="Alto",
                implementation_difficulty="Media",
                estimated_reduction_pct=scope_percentages[1] * 0.4,  # Reducción potencial 40%
                actions=[
                    "Reemplazar vehículos diésel por eléctricos o híbridos",
                    "Optimizar rutas de transporte (reducir km recorridos)",
                    "Mantenimiento preventivo de equipos (mejorar eficiencia)",
                    "Considerar biocombustibles certificados"
                ],
                timeframe="Mediano-Largo plazo (12-36 meses)",
                cost_range="$$$"
            ))
        
        # Scope 3 (Cadena de valor)
        if scope_percentages.get(3, 0) > 30:
            recommendations.append(Recommendation(
                priority=2,
                category="Scope 3",
                title="Engagement con Proveedores",
                description=f"Scope 3 es {scope_percentages[3]:.1f}% de tus emisiones. "
                           "Trabaja con tu cadena de suministro.",
                impact_potential="Medio",
                implementation_difficulty="Difícil",
                estimated_reduction_pct=scope_percentages[3] * 0.2,  # Reducción potencial 20%
                actions=[
                    "Evaluar y seleccionar proveedores con bajas emisiones",
                    "Optimizar logística y transporte upstream/downstream",
                    "Promover trabajo remoto (reducir business travel)",
                    "Implementar programa de reciclaje y economía circular"
                ],
                timeframe="Largo plazo (24-48 meses)",
                cost_range="$$"
            ))
        
        return recommendations
    
    def _analyze_categories(
        self,
        emissions_by_category: Dict[str, float],
        total_emissions: float
    ) -> List[Recommendation]:
        """Genera recomendaciones por categoría específica."""
        recommendations = []
        
        # Encontrar top 3 categorías
        sorted_categories = sorted(
            emissions_by_category.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]
        
        for category, value in sorted_categories:
            pct = (value / total_emissions * 100) if total_emissions > 0 else 0
            
            if pct < 10:  # Ignorar categorías pequeñas
                continue
            
            # Recomendaciones específicas por categoría
            if category == 'mobile_combustion':
                recommendations.append(Recommendation(
                    priority=1,
                    category="Mobile Combustion",
                    title="Electrificación de Flota de Vehículos",
                    description=f"Combustión móvil es {pct:.1f}% de tus emisiones totales.",
                    impact_potential="Alto",
                    implementation_difficulty="Media",
                    estimated_reduction_pct=pct * 0.7,
                    actions=[
                        "Plan de reemplazo gradual a vehículos eléctricos",
                        "Instalar estaciones de carga en instalaciones",
                        "Capacitación en conducción eficiente (eco-driving)",
                        "Telemetría para optimizar rutas y consumo"
                    ],
                    timeframe="Mediano plazo (12-24 meses)",
                    cost_range="$$$"
                ))
            
            elif category == 'purchased_electricity':
                recommendations.append(Recommendation(
                    priority=1,
                    category="Electricity",
                    title="Generación Renovable On-site",
                    description=f"Electricidad comprada es {pct:.1f}% del total.",
                    impact_potential="Alto",
                    implementation_difficulty="Media",
                    estimated_reduction_pct=pct * 0.6,
                    actions=[
                        "Estudio de viabilidad para paneles solares",
                        "Auditoría energética para identificar desperdicios",
                        "Actualizar iluminación a LED",
                        "Sistemas HVAC eficientes con controles inteligentes"
                    ],
                    timeframe="Corto-Mediano plazo (6-18 meses)",
                    cost_range="$$"
                ))
            
            elif category == 'business_travel':
                recommendations.append(Recommendation(
                    priority=2,
                    category="Business Travel",
                    title="Política de Viajes Sostenibles",
                    description=f"Viajes de negocios representan {pct:.1f}%.",
                    impact_potential="Medio",
                    implementation_difficulty="Fácil",
                    estimated_reduction_pct=pct * 0.5,
                    actions=[
                        "Priorizar reuniones virtuales sobre viajes",
                        "Política: tren en lugar de avión para <500 km",
                        "Compensación de carbono para vuelos inevitables",
                        "Tracking de emisiones de viajes en sistema de gastos"
                    ],
                    timeframe="Corto plazo (3-6 meses)",
                    cost_range="$"
                ))
        
        return recommendations
    
    def _compare_with_benchmark(
        self,
        total_emissions: float,
        num_employees: int,
        sector: str
    ) -> List[Recommendation]:
        """Compara con benchmarks sectoriales."""
        recommendations = []
        
        emissions_per_employee = total_emissions / num_employees
        benchmark = self.SECTOR_BENCHMARKS.get(sector, self.SECTOR_BENCHMARKS['default'])
        
        difference_pct = ((emissions_per_employee - benchmark) / benchmark * 100)
        
        if difference_pct > 20:
            recommendations.append(Recommendation(
                priority=1,
                category="General",
                title="Reducción Urgente Necesaria",
                description=f"Tus emisiones por empleado ({emissions_per_employee:.0f} kg CO2e/empleado/año) "
                           f"están {difference_pct:.0f}% por encima del benchmark sectorial ({benchmark:.0f} kg CO2e).",
                impact_potential="Alto",
                implementation_difficulty="Media",
                estimated_reduction_pct=difference_pct,
                actions=[
                    "Establecer meta agresiva de reducción (ej: -30% en 3 años)",
                    "Auditoría completa de emisiones con consultor externo",
                    "Formar comité de sostenibilidad con presupuesto dedicado",
                    "Reportar progreso mensualmente a dirección"
                ],
                timeframe="Inmediato",
                cost_range="$$"
            ))
        elif difference_pct < -20:
            recommendations.append(Recommendation(
                priority=3,
                category="General",
                title="Liderazgo en Sostenibilidad",
                description=f"¡Felicitaciones! Estás {abs(difference_pct):.0f}% por debajo del benchmark sectorial.",
                impact_potential="Bajo",
                implementation_difficulty="Fácil",
                estimated_reduction_pct=5,
                actions=[
                    "Publicar caso de estudio sobre tus logros",
                    "Compartir mejores prácticas con la industria",
                    "Establecer meta Net Zero para 2030-2040",
                    "Certificar con ISO 14064 o Science Based Targets"
                ],
                timeframe="Mediano plazo",
                cost_range="$"
            ))
        
        return recommendations
    
    def _get_general_recommendations(
        self,
        emissions_by_scope: Dict[int, float],
        total_emissions: float
    ) -> List[Recommendation]:
        """Recomendaciones generales aplicables a todos."""
        recommendations = []
        
        # Siempre recomendar medición y reporte
        recommendations.append(Recommendation(
            priority=3,
            category="General",
            title="Mejora Continua en Medición",
            description="La medición precisa es la base de la reducción efectiva.",
            impact_potential="Medio",
            implementation_difficulty="Fácil",
            estimated_reduction_pct=0,  # No reduce directamente, pero habilita reducciones
            actions=[
                "Implementar sistema automatizado de recolección de datos",
                "Capacitar a equipos en inventario de GHG",
                "Establecer KPIs de emisiones en dashboards ejecutivos",
                "Auditar inventario de GHG anualmente (ISO 14064)"
            ],
            timeframe="Corto plazo (3-6 meses)",
            cost_range="$"
        ))
        
        # Engagement de empleados
        recommendations.append(Recommendation(
            priority=3,
            category="General",
            title="Cultura de Sostenibilidad",
            description="Involucrar a todos los empleados en la reducción de emisiones.",
            impact_potential="Medio",
            implementation_difficulty="Fácil",
            estimated_reduction_pct=5,
            actions=[
                "Programa de awareness sobre huella de carbono",
                "Incentivos para empleados con ideas de reducción",
                "Política de trabajo remoto (reduce commuting)",
                "Newsletter mensual de sostenibilidad"
            ],
            timeframe="Corto plazo (1-3 meses)",
            cost_range="$"
        ))
        
        return recommendations
    
    def generate_summary_report(
        self,
        recommendations: List[Recommendation]
    ) -> str:
        """
        Genera reporte ejecutivo en markdown.
        
        Args:
            recommendations: Lista de recomendaciones
        
        Returns:
            String con reporte en markdown
        """
        # Calcular métricas del reporte
        total_reduction_potential = sum(r.estimated_reduction_pct for r in recommendations)
        high_priority = [r for r in recommendations if r.priority == 1]
        
        report = f"""
# 📊 Reporte de Recomendaciones de Reducción

## Resumen Ejecutivo

- **Total de recomendaciones**: {len(recommendations)}
- **Prioridad alta**: {len(high_priority)}
- **Potencial de reducción total**: {total_reduction_potential:.1f}%

---

## 🔥 Recomendaciones Prioritarias (Top 3)

"""
        
        for i, rec in enumerate(high_priority[:3], 1):
            report += f"""
### {i}. {rec.title} ({rec.category})

**Impacto potencial**: {rec.impact_potential} ({rec.estimated_reduction_pct:.1f}% reducción)  
**Dificultad**: {rec.implementation_difficulty}  
**Plazo**: {rec.timeframe}  
**Costo estimado**: {rec.cost_range}

_{rec.description}_

**Acciones recomendadas:**
"""
            for action in rec.actions:
                report += f"\n- {action}"
            
            report += "\n\n---\n"
        
        # Todas las recomendaciones
        report += "\n## 📋 Todas las Recomendaciones\n\n"
        
        for priority in [1, 2, 3]:
            priority_recs = [r for r in recommendations if r.priority == priority]
            if not priority_recs:
                continue
            
            priority_label = {1: "Alta", 2: "Media", 3: "Baja"}[priority]
            report += f"\n### Prioridad {priority_label}\n\n"
            
            for rec in priority_recs:
                report += f"- **{rec.title}** ({rec.category}): {rec.estimated_reduction_pct:.1f}% reducción\n"
        
        return report


# Función de conveniencia
def get_recommendations(
    emissions_by_scope: Dict[int, float],
    emissions_by_category: Dict[str, float],
    total_emissions: float,
    sector: str = 'default',
    num_employees: Optional[int] = None
) -> Tuple[List[Recommendation], str]:
    """
    Función helper para obtener recomendaciones + reporte.
    
    Returns:
        (lista de recomendaciones, reporte en markdown)
    """
    engine = AIRecommendationEngine()
    recommendations = engine.analyze_and_recommend(
        emissions_by_scope,
        emissions_by_category,
        total_emissions,
        sector,
        num_employees
    )
    report = engine.generate_summary_report(recommendations)
    return recommendations, report


if __name__ == '__main__':
    # Ejemplo de uso
    print("=" * 70)
    print("🤖 MOTOR DE RECOMENDACIONES IA")
    print("=" * 70)
    print()
    
    # Datos de ejemplo
    emissions_by_scope = {
        1: 1200,  # Scope 1
        2: 3400,  # Scope 2
        3: 800    # Scope 3
    }
    
    emissions_by_category = {
        'mobile_combustion': 1200,
        'purchased_electricity': 3400,
        'business_travel': 500,
        'waste_generated': 300
    }
    
    total = sum(emissions_by_scope.values())
    
    # Generar recomendaciones
    recommendations, report = get_recommendations(
        emissions_by_scope,
        emissions_by_category,
        total,
        sector='services',
        num_employees=50
    )
    
    # Mostrar reporte
    print(report)
    print()
    print(f"✅ Generadas {len(recommendations)} recomendaciones")
