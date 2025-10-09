"""
Asistente de IA Local para Categorización de Emisiones.
Usa Ollama local (100% gratuito, sin APIs de pago).

Funcionalidades:
1. Categorización automática de actividades
2. Búsqueda semántica de factores de emisión
3. Recomendaciones inteligentes basadas en datos
"""

import json
import requests
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import logging

# Configuración
OLLAMA_API_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "llama3:latest"  # Usar el modelo disponible

logger = logging.getLogger(__name__)


@dataclass
class CategorizationResult:
    """Resultado de categorización automática."""
    scope: int
    category: str
    fuel_type: Optional[str] = None
    confidence: float = 0.0
    explanation: str = ""
    suggestions: List[str] = None
    
    def __post_init__(self):
        if self.suggestions is None:
            self.suggestions = []


@dataclass
class FactorMatch:
    """Resultado de búsqueda semántica de factor."""
    factor_name: str
    value: float
    unit: str
    source: str
    year: int
    match_score: float
    category: str
    geography: Optional[str] = None
    
    # Atributos adicionales para compatibilidad con tests
    activity: str = ""
    fuel: str = ""
    sheet: str = ""
    
    def __post_init__(self):
        # Alias para compatibilidad
        if not self.sheet:
            self.sheet = self.category
        if not self.activity and self.factor_name:
            # Extraer activity del factor_name
            parts = self.factor_name.split(' - ')
            if len(parts) >= 2:
                self.activity = parts[0]
                self.fuel = parts[1]
            else:
                self.activity = self.factor_name
    
    @property
    def relevance_score(self):
        """Alias para match_score para compatibilidad con tests."""
        return self.match_score


class GHGCategoryMapper:
    """
    Mapeador de categorías GHG Protocol usando IA local.
    
    Usa Ollama con llama3.2 para categorización inteligente
    de actividades en lenguaje natural.
    """
    
    # Mapeo de categorías con scopes y keywords para fallback
    CATEGORY_MAP = {
        'stationary_combustion': {
            'scope': 1,
            'keywords': ['diesel', 'gasolina', 'combustible', 'caldera', 'generador', 'fijo', 'estacionario']
        },
        'mobile_combustion': {
            'scope': 1,
            'keywords': ['vehículo', 'camión', 'auto', 'tractor', 'móvil', 'transporte propio']
        },
        'fugitive_emissions': {
            'scope': 1,
            'keywords': ['refrigerante', 'fuga', 'aire acondicionado', 'r-410a', 'r-134a']
        },
        'purchased_electricity': {
            'scope': 2,
            'keywords': ['electricidad', 'energía eléctrica', 'kwh', 'power']
        },
        'purchased_heat_steam': {
            'scope': 2,
            'keywords': ['calor', 'vapor', 'heating', 'steam']
        },
        'business_travel': {
            'scope': 3,
            'keywords': ['vuelo', 'viaje', 'hotel', 'avión', 'negocios']
        },
        'employee_commuting': {
            'scope': 3,
            'keywords': ['commuting', 'empleado', 'transporte personal', 'casa trabajo']
        },
        'upstream_transportation': {
            'scope': 3,
            'keywords': ['transporte', 'flete', 'freight', 'envío', 'logística']
        },
        'waste_generated': {
            'scope': 3,
            'keywords': ['residuo', 'basura', 'desecho', 'waste']
        },
        'purchased_goods': {
            'scope': 3,
            'keywords': ['compra', 'insumo', 'materia prima', 'bienes']
        }
    }
    
    def __init__(self, model: str = DEFAULT_MODEL, api_url: str = OLLAMA_API_URL):
        self.model = model
        self.api_url = api_url
        self.context = self._build_ghg_context()
    
    def _build_ghg_context(self) -> str:
        """Construye contexto del GHG Protocol para el LLM."""
        return """Eres un experto en GHG Protocol y medición de huella de carbono.

SCOPES DEL GHG PROTOCOL:

Scope 1 (Emisiones Directas):
- stationary_combustion: Combustión en calderas, hornos, generadores fijos
  Ejemplos: gas natural en calderas, diesel en generadores, fuel oil en hornos
- mobile_combustion: Vehículos y maquinaria móvil de la organización
  Ejemplos: gasolina en autos, diesel en camiones, GLP en montacargas
- process_emissions: Emisiones de procesos industriales
  Ejemplos: producción de cemento, cal, vidrio, químicos
- fugitive_emissions: Fugas de refrigerantes, aire acondicionado, sistemas
  Ejemplos: refrigerantes R-410A, SF6, fugas de gas natural

Scope 2 (Emisiones Indirectas de Energía):
- purchased_electricity: Electricidad comprada de la red
- purchased_heat: Calor/vapor comprado de terceros
- purchased_cooling: Refrigeración comprada

Scope 3 (Otras Emisiones Indirectas):
Categorías upstream:
1. purchased_goods_services: Materiales, productos comprados
2. capital_goods: Equipos, maquinaria, construcción
3. fuel_energy_activities: Extracción y transporte de combustibles
4. upstream_transportation: Transporte de insumos
5. waste_generated: Disposición de residuos
6. business_travel: Viajes de negocios (avión, hotel)
7. employee_commuting: Traslados diarios empleados
8. upstream_leased_assets: Activos arrendados upstream

Categorías downstream:
9. downstream_transportation: Distribución de productos
10. processing_sold_products: Procesamiento de productos vendidos
11. use_sold_products: Uso de productos por clientes
12. end_of_life_sold_products: Disposición final de productos
13. downstream_leased_assets: Activos arrendados downstream
14. franchises: Operaciones franquiciadas
15. investments: Inversiones financieras

INSTRUCCIONES:
- Analiza la descripción de la actividad
- Determina el scope (1, 2 o 3)
- Identifica la categoría específica
- Si es combustible, identifica el tipo
- Asigna nivel de confianza (0.0-1.0)
- Proporciona explicación breve
- Sugiere información adicional si es necesaria
"""
    
    def map_activity(self, description: str, activity_value: Optional[float] = None,
                    activity_unit: Optional[str] = None) -> CategorizationResult:
        """
        Mapea una descripción en lenguaje natural a categorías GHG Protocol.
        
        Args:
            description: Descripción de la actividad (ej: "consumo de diesel en tractores")
            activity_value: Valor opcional para contexto
            activity_unit: Unidad opcional para contexto
        
        Returns:
            CategorizationResult con scope, categoría, confianza y explicación
        
        Example:
            >>> mapper = GHGCategoryMapper()
            >>> result = mapper.map_activity("consumo de diesel en tractores agrícolas")
            >>> print(f"Scope {result.scope}: {result.category}")
            Scope 1: mobile_combustion
        """
        # Construir prompt
        prompt = f"""{self.context}

ACTIVIDAD A CATEGORIZAR:
Descripción: {description}
"""
        if activity_value and activity_unit:
            prompt += f"Cantidad: {activity_value} {activity_unit}\n"
        
        prompt += """
RESPONDE EN FORMATO JSON:
{
  "scope": 1 o 2 o 3,
  "category": "nombre_categoria",
  "fuel_type": "tipo de combustible si aplica o null",
  "confidence": 0.0-1.0,
  "explanation": "Explicación breve de por qué esta categoría",
  "suggestions": ["sugerencia1", "sugerencia2"]
}

SOLO RESPONDE CON EL JSON, SIN TEXTO ADICIONAL.
"""
        
        try:
            # Llamar a Ollama API
            response = self._call_ollama(prompt)
            
            # Parsear respuesta
            result = self._parse_response(response)
            return result
            
        except Exception as e:
            logger.error(f"Error en categorización IA: {e}")
            # Fallback a categorización basada en reglas
            return self._fallback_categorization(description)
    
    def _call_ollama(self, prompt: str, max_retries: int = 2) -> str:
        """Llama a la API de Ollama."""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,  # Baja temperatura para respuestas consistentes
                "top_p": 0.9,
                "num_predict": 500
            }
        }
        
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.api_url,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get('response', '')
                else:
                    logger.warning(f"Ollama API error: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                if attempt == 0:
                    logger.warning("Ollama server not running. Starting...")
                    self._try_start_ollama()
                    continue
                else:
                    raise Exception("No se puede conectar a Ollama. Inicia el servidor con 'ollama serve'")
            
            except requests.exceptions.Timeout:
                logger.warning(f"Timeout en intento {attempt + 1}")
                continue
        
        raise Exception("Máximo de intentos alcanzado")
    
    def _try_start_ollama(self):
        """Intenta iniciar el servidor Ollama (Windows)."""
        import subprocess
        try:
            subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NEW_CONSOLE if hasattr(subprocess, 'CREATE_NEW_CONSOLE') else 0
            )
            import time
            time.sleep(3)  # Esperar a que inicie
        except Exception as e:
            logger.warning(f"No se pudo iniciar Ollama automáticamente: {e}")
    
    def _parse_response(self, response: str) -> CategorizationResult:
        """Parsea la respuesta JSON del LLM."""
        # Buscar JSON en la respuesta
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        
        if json_start >= 0 and json_end > json_start:
            json_str = response[json_start:json_end]
            data = json.loads(json_str)
            
            return CategorizationResult(
                scope=int(data['scope']),
                category=data['category'],
                fuel_type=data.get('fuel_type'),
                confidence=float(data['confidence']),
                explanation=data.get('explanation', ''),
                suggestions=data.get('suggestions', [])
            )
        else:
            raise ValueError("No se encontró JSON válido en la respuesta")
    
    def _fallback_categorization(self, description: str) -> CategorizationResult:
        """Categorización basada en reglas como fallback."""
        desc_lower = description.lower()
        
        # Reglas simples basadas en palabras clave
        if any(word in desc_lower for word in ['diesel', 'gasolina', 'gasoline', 'fuel']):
            if any(word in desc_lower for word in ['vehículo', 'camión', 'auto', 'tractor', 'móvil', 'vehicle']):
                return CategorizationResult(
                    scope=1,
                    category='mobile_combustion',
                    fuel_type='diesel' if 'diesel' in desc_lower else 'gasoline',
                    confidence=0.8,
                    explanation='Combustible en vehículo móvil = Scope 1 mobile_combustion',
                    suggestions=['Especifica el tipo de vehículo para mayor precisión']
                )
            else:
                return CategorizationResult(
                    scope=1,
                    category='stationary_combustion',
                    fuel_type='diesel' if 'diesel' in desc_lower else 'fuel',
                    confidence=0.7,
                    explanation='Combustible en equipo fijo = Scope 1 stationary_combustion',
                    suggestions=['¿Es un generador, caldera u otro equipo fijo?']
                )
        
        elif any(word in desc_lower for word in ['electricidad', 'electricity', 'kwh', 'energía eléctrica']):
            return CategorizationResult(
                scope=2,
                category='purchased_electricity',
                confidence=0.9,
                explanation='Consumo de electricidad = Scope 2',
                suggestions=['Confirma si la electricidad es comprada de la red']
            )
        
        elif any(word in desc_lower for word in ['refrigerante', 'refrigerant', 'aire acondicionado', 'ac', 'fuga']):
            return CategorizationResult(
                scope=1,
                category='fugitive_emissions',
                confidence=0.85,
                explanation='Refrigerantes/fugas = Scope 1 fugitive_emissions',
                suggestions=['Especifica el tipo de refrigerante (ej: R-410A, R-134a)']
            )
        
        elif any(word in desc_lower for word in ['vuelo', 'flight', 'viaje', 'avión', 'hotel']):
            return CategorizationResult(
                scope=3,
                category='business_travel',
                confidence=0.8,
                explanation='Viajes de negocios = Scope 3 business_travel',
                suggestions=['Especifica distancia o tipo de transporte']
            )
        
        elif any(word in desc_lower for word in ['residuo', 'waste', 'basura', 'desecho']):
            return CategorizationResult(
                scope=3,
                category='waste_generated',
                confidence=0.75,
                explanation='Generación de residuos = Scope 3 waste_generated',
                suggestions=['Indica tipo de residuo (orgánico, reciclable, peligroso)']
            )
        
        elif any(word in desc_lower for word in ['transporte', 'freight', 'flete', 'envío']):
            return CategorizationResult(
                scope=3,
                category='upstream_transportation',
                confidence=0.7,
                explanation='Transporte de mercancías = Scope 3 upstream_transportation',
                suggestions=['¿Es transporte de insumos (upstream) o de productos vendidos (downstream)?']
            )
        
        else:
            # No hay coincidencia clara
            return CategorizationResult(
                scope=1,
                category='stationary_combustion',
                confidence=0.3,
                explanation='No se pudo determinar con certeza. Categoría por defecto.',
                suggestions=[
                    'Proporciona más detalles sobre la actividad',
                    '¿Es combustión, electricidad, transporte, residuos u otro?',
                    'Especifica si es equipo propio o de terceros'
                ]
            )
    
    def batch_categorize(self, descriptions: List[str]) -> List[CategorizationResult]:
        """Categoriza múltiples actividades en batch."""
        results = []
        for desc in descriptions:
            result = self.map_activity(desc)
            results.append(result)
        return results


class SemanticFactorSearch:
    """
    Búsqueda semántica de factores de emisión usando IA.
    
    Permite encontrar factores relevantes aunque la descripción
    no coincida exactamente con el nombre del factor.
    
    Características:
    - Búsqueda multi-nivel (exacta, sinónimos, fuzzy)
    - Categorización automática antes de buscar
    - Scoring con pesos por relevancia
    - Cache de resultados frecuentes
    """
    
    # Diccionario de sinónimos para mejorar búsqueda
    SYNONYMS = {
        'diesel': ['diésel', 'gasoil', 'diesel fuel', 'automotive diesel'],
        'gasoline': ['gasolina', 'petrol', 'nafta', 'gas'],
        'electricity': ['electricidad', 'energía eléctrica', 'power', 'kwh'],
        'natural_gas': ['gas natural', 'natural gas', 'lng', 'gnl'],
        'truck': ['camión', 'camion', 'lorry', 'freight vehicle'],
        'car': ['auto', 'coche', 'vehículo', 'automobile', 'vehicle'],
        'flight': ['vuelo', 'avión', 'airplane', 'aircraft', 'aviation'],
        'ship': ['barco', 'buque', 'vessel', 'maritime', 'marítimo'],
        'train': ['tren', 'ferrocarril', 'rail', 'railway'],
        'waste': ['residuo', 'basura', 'desecho', 'garbage'],
        'refrigerant': ['refrigerante', 'coolant', 'r-410a', 'r-134a'],
    }
    
    def __init__(self, factors_df, model: str = DEFAULT_MODEL):
        """
        Args:
            factors_df: DataFrame con factores de emisión
            model: Modelo Ollama a usar
        """
        self.factors_df = factors_df
        self.model = model
        self.api_url = OLLAMA_API_URL
        self._search_cache = {}
        
        # Pre-procesar factores para búsqueda rápida
        self._build_search_index()
    
    def _build_search_index(self):
        """Construye índice de búsqueda para factores."""
        self.search_index = []
        
        for idx, row in self.factors_df.iterrows():
            # Combinar todos los campos de texto disponibles
            # Las columnas reales son: Activity, Fuel, Unit, Source, Sheet
            searchable_text = ' '.join([
                str(row.get('Activity', '')),
                str(row.get('Fuel', '')),
                str(row.get('Sheet', '')),
                str(row.get('Unit', ''))
            ]).lower()
            
            self.search_index.append({
                'idx': idx,
                'text': searchable_text,
                'activity': str(row.get('Activity', '')),
                'fuel': str(row.get('Fuel', '')),
                'sheet': str(row.get('Sheet', '')),
                'value': float(row.get('kgCO2e', 0)),
                'unit': str(row.get('Unit', ''))
            })
    
    def search(self, query: str, top_k: int = 5, 
               category_hint: Optional[str] = None) -> List[FactorMatch]:
        """
        Busca factores relevantes usando búsqueda semántica mejorada.
        
        Args:
            query: Descripción en lenguaje natural
            top_k: Número de resultados a devolver
            category_hint: Categoría para filtrar (ej: 'Fuels', 'Electricity')
        
        Returns:
            Lista de FactorMatch ordenados por relevancia
        
        Example:
            >>> searcher = SemanticFactorSearch(factors_df)
            >>> results = searcher.search("transporte marítimo de contenedores")
            >>> for r in results:
            >>>     print(f"{r.factor_name}: {r.value} {r.unit}")
        """
        # Manejar consulta vacía
        if not query or not query.strip():
            return []
        
        # Verificar cache
        cache_key = f"{query}_{top_k}_{category_hint}"
        if cache_key in self._search_cache:
            return self._search_cache[cache_key]
        
        # Expandir query con sinónimos
        expanded_query = self._expand_with_synonyms(query)
        
        # Búsqueda multi-nivel
        results = self._multi_level_search(expanded_query, category_hint)
        
        # Ordenar y limitar
        results.sort(key=lambda x: x.match_score, reverse=True)
        top_results = results[:top_k]
        
        # Guardar en cache
        self._search_cache[cache_key] = top_results
        
        return top_results
    
    def _expand_with_synonyms(self, query: str) -> List[str]:
        """Expande query con sinónimos."""
        terms = [query.lower()]
        
        for word, synonyms in self.SYNONYMS.items():
            if word in query.lower():
                terms.extend(synonyms)
        
        return terms
    
    def _multi_level_search(self, query_terms: List[str], 
                           category_hint: Optional[str]) -> List[FactorMatch]:
        """Búsqueda multi-nivel con scoring."""
        matches = []
        
        for item in self.search_index:
            # Filtrar por categoría si se proporciona (usando Sheet)
            if category_hint and category_hint.lower() not in item['sheet'].lower():
                continue
            
            # Calcular score
            score = self._calculate_match_score(query_terms, item)
            
            if score > 0.1:  # Umbral mínimo
                match = FactorMatch(
                    factor_name=f"{item['activity']} - {item['fuel']}" if item['fuel'] and item['fuel'] != 'nan' else item['activity'],
                    value=item['value'],
                    unit=item['unit'],
                    source="UK Gov 2025",
                    year=2025,
                    match_score=score,
                    category=item['sheet'],
                    geography='GBR',
                    activity=item['activity'],
                    fuel=item['fuel'],
                    sheet=item['sheet']
                )
                matches.append(match)
        
        return matches
    
    def _calculate_match_score(self, query_terms: List[str], item: dict) -> float:
        """
        Calcula score de coincidencia con pesos.
        
        Pesos:
        - Coincidencia exacta: 1.0
        - En Activity (categoría principal): 0.8
        - En Fuel (subcategoría): 0.6
        - En Sheet (tipo): 0.4
        - En Unit: 0.2
        """
        score = 0.0
        text = item['text']
        
        for term in query_terms:
            term_lower = term.lower()
            
            # Coincidencia exacta (frase completa)
            if term_lower in text:
                score += 1.0
            
            # Palabras individuales con pesos
            words = term_lower.split()
            for word in words:
                if len(word) <= 2:  # Ignorar palabras muy cortas
                    continue
                
                # Peso según dónde aparezca
                if word in item['activity'].lower():
                    score += 0.8
                elif word in item['fuel'].lower():
                    score += 0.6
                elif word in item['sheet'].lower():
                    score += 0.4
                elif word in item['unit'].lower():
                    score += 0.2
        
        # Normalizar por número de términos
        if query_terms:
            score = score / len(query_terms)
        
        return min(score, 1.0)  # Máximo 1.0
    
    def search_with_category(self, description: str, top_k: int = 3) -> List[FactorMatch]:
        """
        Busca factores usando primero categorización IA.
        
        Este método:
        1. Categoriza la actividad con IA
        2. Filtra factores por categoría (Sheet)
        3. Busca los mejores matches
        
        Args:
            description: Descripción completa de la actividad
            top_k: Número de resultados
        
        Returns:
            Lista de FactorMatch más relevantes
        """
        # Categorizar primero
        mapper = GHGCategoryMapper()
        categorization = mapper.map_activity(description)
        
        # Mapear categoría a Sheet del Excel
        category_mapping = {
            'mobile_combustion': 'Fuels',
            'stationary_combustion': 'Fuels',
            'purchased_electricity': 'UK electricity',
            'fugitive_emissions': 'Refrigerant',
            'business_travel': 'Business travel',
            'waste_generated': 'Waste disposal',
            'upstream_transportation': 'Freighting goods'
        }
        
        category_hint = category_mapping.get(categorization.category)
        
        # Buscar con hint de categoría
        return self.search(description, top_k, category_hint)


def check_ollama_status() -> Dict[str, bool]:
    """
    Verifica el estado de Ollama.
    
    Returns:
        Dict con 'installed', 'running', 'model_available'
    """
    status = {
        'installed': False,
        'running': False,
        'model_available': False,
        'models': []
    }
    
    # Verificar instalación
    import shutil
    if shutil.which('ollama'):
        status['installed'] = True
    
    # Verificar si está corriendo
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            status['running'] = True
            models = response.json().get('models', [])
            status['models'] = [m['name'] for m in models]
            
            # Verificar si llama3.2 está disponible
            if any('llama3.2' in m for m in status['models']):
                status['model_available'] = True
    except:
        pass
    
    return status


if __name__ == "__main__":
    # Ejemplo de uso
    print("🤖 Testing IA Assistant para GHG Protocol\n")
    
    # Verificar estado de Ollama
    status = check_ollama_status()
    print(f"Ollama instalado: {status['installed']}")
    print(f"Ollama corriendo: {status['running']}")
    print(f"Modelos disponibles: {status['models']}\n")
    
    if not status['running']:
        print("⚠️ Ollama no está corriendo.")
        print("Inicia el servidor con: ollama serve")
        print("Descarga modelo con: ollama pull llama3.2:3b\n")
        print("Usando categorización basada en reglas...\n")
    
    # Test categorización
    mapper = GHGCategoryMapper()
    
    test_cases = [
        "consumo de diesel en tractores agrícolas",
        "electricidad comprada de la red en oficina",
        "vuelos de negocios a conferencia internacional",
        "fuga de refrigerante R-410A del aire acondicionado",
        "residuos orgánicos enviados a relleno sanitario",
        "gas natural en calderas para calefacción"
    ]
    
    print("📊 RESULTADOS DE CATEGORIZACIÓN:\n")
    for desc in test_cases:
        result = mapper.map_activity(desc)
        print(f"📝 '{desc}'")
        print(f"   ➜ Scope {result.scope}: {result.category}")
        print(f"   ➜ Confianza: {result.confidence:.0%}")
        print(f"   ➜ {result.explanation}")
        if result.fuel_type:
            print(f"   ➜ Combustible: {result.fuel_type}")
        print()
