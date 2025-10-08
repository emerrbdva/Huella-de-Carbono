"""Script de prueba para el asistente de IA."""
import sys
from pathlib import Path

# Agregar path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.ai_assistant import GHGCategoryMapper, check_ollama_status

def main():
    print("🤖 Testing IA Assistant para GHG Protocol\n")
    
    # Verificar estado de Ollama
    status = check_ollama_status()
    print(f"✓ Ollama instalado: {'SÍ' if status['installed'] else 'NO'}")
    print(f"✓ Ollama corriendo: {'SÍ' if status['running'] else 'NO'}")
    print(f"✓ Modelos disponibles: {', '.join(status['models']) if status['models'] else 'Ninguno'}\n")
    
    if not status['running']:
        print("⚠️  Ollama no está corriendo.")
        print("   Inicia el servidor con: ollama serve")
        print("   Descarga modelo con: ollama pull llama3.2:3b\n")
        print("📝 Usando categorización basada en reglas (FALLBACK)...\n")
    else:
        print("✅ Ollama está listo! Usando IA completa.\n")
    
    # Test categorización
    mapper = GHGCategoryMapper()
    
    test_cases = [
        "consumo de diesel en tractores agrícolas",
        "electricidad comprada de la red en oficina",
        "vuelos de negocios a conferencia internacional",
        "fuga de refrigerante R-410A del aire acondicionado",
        "residuos orgánicos enviados a relleno sanitario",
        "gas natural en calderas para calefacción",
        "transporte de materias primas en camiones"
    ]
    
    print("="*70)
    print("📊 RESULTADOS DE CATEGORIZACIÓN AUTOMÁTICA")
    print("="*70 + "\n")
    
    for i, desc in enumerate(test_cases, 1):
        print(f"{i}. 📝 '{desc}'")
        try:
            result = mapper.map_activity(desc)
            print(f"   ✓ Scope {result.scope}: {result.category}")
            print(f"   ✓ Confianza: {result.confidence:.0%}")
            print(f"   ✓ Explicación: {result.explanation}")
            if result.fuel_type:
                print(f"   ✓ Combustible identificado: {result.fuel_type}")
            if result.suggestions:
                print(f"   💡 Sugerencias:")
                for sug in result.suggestions:
                    print(f"      - {sug}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        print()
    
    print("="*70)
    print("✅ Test completado!")
    print("="*70)

if __name__ == "__main__":
    main()
