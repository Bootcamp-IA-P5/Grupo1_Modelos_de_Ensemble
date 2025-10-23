"""
Dashboard simple para ver estadísticas de A/B Testing
"""

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from src.api.services.ab_testing_service import ab_testing_service
import json

router = APIRouter()

@router.get("/dashboard", response_class=HTMLResponse)
async def ab_testing_dashboard():
    """
    Dashboard HTML simple para ver estadísticas de A/B Testing
    """
    try:
        stats = ab_testing_service.get_model_stats()
        
        # Crear HTML del dashboard
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>A/B Testing Dashboard - EcoPrint AI</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: #333;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 15px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                    overflow: hidden;
                }}
                .header {{
                    background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 2.5em;
                    font-weight: 300;
                }}
                .header p {{
                    margin: 10px 0 0 0;
                    opacity: 0.9;
                    font-size: 1.1em;
                }}
                .content {{
                    padding: 30px;
                }}
                .stats-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 20px;
                    margin-bottom: 30px;
                }}
                .stat-card {{
                    background: #f8f9fa;
                    border-radius: 10px;
                    padding: 20px;
                    border-left: 5px solid #3498db;
                    transition: transform 0.3s ease;
                }}
                .stat-card:hover {{
                    transform: translateY(-5px);
                    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                }}
                .stat-card h3 {{
                    margin: 0 0 15px 0;
                    color: #2c3e50;
                    font-size: 1.3em;
                }}
                .stat-item {{
                    display: flex;
                    justify-content: space-between;
                    margin: 10px 0;
                    padding: 8px 0;
                    border-bottom: 1px solid #ecf0f1;
                }}
                .stat-label {{
                    font-weight: 600;
                    color: #7f8c8d;
                }}
                .stat-value {{
                    font-weight: bold;
                    color: #2c3e50;
                }}
                .model-performance {{
                    background: #fff;
                    border-radius: 10px;
                    padding: 20px;
                    margin-top: 20px;
                    border: 1px solid #ecf0f1;
                }}
                .model-card {{
                    background: #f8f9fa;
                    border-radius: 8px;
                    padding: 15px;
                    margin: 10px 0;
                    border-left: 4px solid #e74c3c;
                }}
                .model-card.xgboost {{ border-left-color: #27ae60; }}
                .model-card.random_forest {{ border-left-color: #f39c12; }}
                .model-card.extra_trees {{ border-left-color: #9b59b6; }}
                .refresh-btn {{
                    background: #3498db;
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 6px;
                    cursor: pointer;
                    font-size: 16px;
                    margin: 20px 0;
                    transition: background 0.3s ease;
                }}
                .refresh-btn:hover {{
                    background: #2980b9;
                }}
                .timestamp {{
                    text-align: center;
                    color: #7f8c8d;
                    font-size: 0.9em;
                    margin-top: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🧪 A/B Testing Dashboard</h1>
                    <p>Monitoreo en tiempo real de modelos de Machine Learning</p>
                </div>
                <div class="content">
                    <button class="refresh-btn" onclick="location.reload()">🔄 Actualizar Datos</button>
                    
                    <div class="stats-grid">
                        <div class="stat-card">
                            <h3>📊 Resumen General</h3>
                            <div class="stat-item">
                                <span class="stat-label">Modelos Cargados:</span>
                                <span class="stat-value">{len(stats['models_loaded'])}</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-label">Total Predicciones:</span>
                                <span class="stat-value">{sum(model.get('total_predictions', 0) for model in stats['model_performance'].values())}</span>
                            </div>
                        </div>
                        
                        <div class="stat-card">
                            <h3>⚖️ Distribución de Tráfico</h3>
                            {''.join([f'''
                            <div class="stat-item">
                                <span class="stat-label">{model.replace('_', ' ').title()}:</span>
                                <span class="stat-value">{weight*100:.1f}%</span>
                            </div>''' for model, weight in stats['model_weights'].items()])}
                        </div>
                    </div>
                    
                    <div class="model-performance">
                        <h3>🤖 Rendimiento por Modelo</h3>
                        {''.join([f'''
                        <div class="model-card {model}">
                            <h4>{model.replace('_', ' ').title()}</h4>
                            <div class="stat-item">
                                <span class="stat-label">Predicciones:</span>
                                <span class="stat-value">{perf.get('total_predictions', 0)}</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-label">Confianza Promedio:</span>
                                <span class="stat-value">{perf.get('avg_confidence', 0):.3f}</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-label">Tiempo Promedio:</span>
                                <span class="stat-value">{perf.get('avg_processing_time', 0):.1f}ms</span>
                            </div>
                        </div>''' for model, perf in stats['model_performance'].items()])}
                    </div>
                    
                    <div class="timestamp">
                        Última actualización: {stats.get('timestamp', 'N/A')}
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        return HTMLResponse(content=html_content)
        
    except Exception as e:
        error_html = f"""
        <html>
        <body style="font-family: Arial; padding: 20px; background: #f8f9fa;">
            <h1>❌ Error en Dashboard</h1>
            <p>Error: {str(e)}</p>
            <a href="/ab-testing/stats">Ver datos en JSON</a>
        </body>
        </html>
        """
        return HTMLResponse(content=error_html, status_code=500)
