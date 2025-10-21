// Script de inicialización de MongoDB para EcoPrint AI
// Crea las colecciones necesarias y configura índices

// Usar la base de datos ensemble_models
db = db.getSiblingDB('ensemble_models');

// ===========================================
// Crear colecciones
// ===========================================

// Colección de predicciones
db.createCollection('predictions', {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["features", "prediction", "class_name", "confidence", "risk_level", "risk_score", "timestamp"],
      properties: {
        features: {
          bsonType: "array",
          items: { bsonType: "double" },
          minItems: 54,
          maxItems: 54
        },
        prediction: { bsonType: "int", minimum: 0, maximum: 6 },
        class_name: { bsonType: "string" },
        confidence: { bsonType: "double", minimum: 0, maximum: 1 },
        risk_level: { bsonType: "string", enum: ["LOW", "MEDIUM", "HIGH"] },
        risk_score: { bsonType: "int", minimum: 1, maximum: 9 },
        processing_time_ms: { bsonType: "double" },
        user_id: { bsonType: "string" },
        location: {
          bsonType: "object",
          properties: {
            lat: { bsonType: "double" },
            lon: { bsonType: "double" }
          }
        },
        timestamp: { bsonType: "date" }
      }
    }
  }
});

// Colección de feedback
db.createCollection('feedback', {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["prediction_id", "feedback_type", "rating", "timestamp"],
      properties: {
        prediction_id: { bsonType: "string" },
        feedback_type: { bsonType: "string" },
        rating: { bsonType: "string", enum: ["very_poor", "poor", "average", "good", "excellent"] },
        comment: { bsonType: "string" },
        user_id: { bsonType: "string" },
        timestamp: { bsonType: "date" }
      }
    }
  }
});

// Colección de métricas
db.createCollection('metrics', {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["timestamp", "metric_type"],
      properties: {
        metric_type: { bsonType: "string" },
        data: { bsonType: "object" },
        timestamp: { bsonType: "date" }
      }
    }
  }
});

// ===========================================
// Crear índices para optimizar consultas
// ===========================================

// Índices para predicciones
db.predictions.createIndex({ "timestamp": -1 });
db.predictions.createIndex({ "user_id": 1 });
db.predictions.createIndex({ "prediction": 1 });
db.predictions.createIndex({ "risk_level": 1 });
db.predictions.createIndex({ "confidence": -1 });

// Índices para feedback
db.feedback.createIndex({ "prediction_id": 1 });
db.feedback.createIndex({ "timestamp": -1 });
db.feedback.createIndex({ "rating": 1 });
db.feedback.createIndex({ "user_id": 1 });

// Índices para métricas
db.metrics.createIndex({ "timestamp": -1 });
db.metrics.createIndex({ "metric_type": 1 });

// ===========================================
// Insertar datos de ejemplo (opcional)
// ===========================================

// Insertar una predicción de ejemplo
db.predictions.insertOne({
  features: [2000.0, 180.0, 15.0, 300.0, 50.0, 1000.0, 200.0, 220.0, 180.0, 2000.0].concat(new Array(44).fill(0.0)),
  prediction: 1,
  class_name: "Lodgepole Pine",
  confidence: 0.95,
  risk_level: "HIGH",
  risk_score: 8,
  processing_time_ms: 45.2,
  user_id: "system_init",
  location: { lat: 40.7128, lon: -74.0060 },
  timestamp: new Date()
});

print("✅ Base de datos inicializada correctamente");
print("✅ Colecciones creadas: predictions, feedback, metrics");
print("✅ Índices creados para optimizar consultas");
print("✅ Datos de ejemplo insertados");
