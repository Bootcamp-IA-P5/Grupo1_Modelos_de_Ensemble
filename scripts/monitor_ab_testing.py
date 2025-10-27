"""
Monitor de A/B Testing en tiempo real
Ejecuta este script para ver estadísticas actualizándose automáticamente
"""

import requests
import time
import os
import json
from datetime import datetime

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_ab_stats():
    """Obtener estadísticas de A/B testing"""
    try:
        response = requests.get("http://localhost:8000/ab-testing/stats", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def display_stats(stats):
    """Mostrar estadísticas de forma bonita"""
    clear_screen()
    
    print("🧪 A/B TESTING MONITOR - TIEMPO REAL")
    print("=" * 50)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    if "error" in stats:
        print(f"❌ Error: {stats['error']}")
        return
    
    ab_stats = stats.get("ab_testing_stats", {})
    
    # Resumen general
    print("📊 RESUMEN GENERAL:")
    print(f"   Modelos cargados: {len(ab_stats.get('models_loaded', []))}")
    total_predictions = sum(
        model.get('total_predictions', 0) 
        for model in ab_stats.get('model_performance', {}).values()
    )
    print(f"   Total predicciones: {total_predictions}")
    print()
    
    # Distribución de tráfico
    print("⚖️  DISTRIBUCIÓN DE TRÁFICO:")
    weights = ab_stats.get('model_weights', {})
    for model, weight in weights.items():
        bar = "█" * int(weight * 20)  # Barra visual
        print(f"   {model.replace('_', ' ').title():15} {weight*100:5.1f}% {bar}")
    print()
    
    # Rendimiento por modelo
    print("🤖 RENDIMIENTO POR MODELO:")
    performance = ab_stats.get('model_performance', {})
    
    for model, perf in performance.items():
        print(f"   {model.replace('_', ' ').title()}:")
        print(f"      Predicciones: {perf.get('total_predictions', 0)}")
        print(f"      Confianza:    {perf.get('avg_confidence', 0):.3f}")
        print(f"      Tiempo:       {perf.get('avg_processing_time', 0):.1f}ms")
        print()
    
    print("💡 Presiona Ctrl+C para salir")
    print("🔄 Actualizando cada 5 segundos...")

def main():
    """Función principal del monitor"""
    print("🚀 Iniciando monitor de A/B Testing...")
    print("   Asegúrate de que el servidor esté corriendo en http://localhost:8000")
    print()
    
    try:
        while True:
            stats = get_ab_stats()
            display_stats(stats)
            time.sleep(5)  # Actualizar cada 5 segundos
            
    except KeyboardInterrupt:
        print("\n\n👋 Monitor detenido. ¡Hasta luego!")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
