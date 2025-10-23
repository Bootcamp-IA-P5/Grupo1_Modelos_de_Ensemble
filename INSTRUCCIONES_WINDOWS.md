# 🖥️ INSTRUCCIONES PARA WINDOWS

## ✅ **SISTEMA MULTIPLATAFORMA LISTO**

El sistema ahora detecta automáticamente si estás en Windows, Mac o Linux y usa la configuración apropiada.

## 🚀 **PASOS PARA WINDOWS:**

### **1. Clonar el repositorio**
```bash
git clone [tu-repositorio]
cd Grupo1_Modelos_de_Ensemble
```

### **2. Crear entorno virtual**
```bash
python -m venv venv
venv\Scripts\activate
```

### **3. Instalar dependencias**
```bash
pip install -r requirements.txt
```

### **4. Configurar variables de entorno**
Crear archivo `.env`:
```env
MONGO_URI=mongodb+srv://barbdeveloper11_db_user:2sn26wQR1C4fQuoC@cluster0.n7u5rn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
DB_NAME=ensemble_models
```

### **5. Probar conexión**
```bash
python test_mongo_universal.py
```

**Debería mostrar:**
```
🖥️  Sistema: Windows 10
🐍 Python: 3.x.x
🔌 PROBANDO MONGODB UNIVERSAL...
✅ Conectado exitosamente!
🎉 ¡MONGODB FUNCIONANDO EN TODAS LAS PLATAFORMAS!
```

### **6. Iniciar servidor**
```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### **7. Probar API**
```bash
curl http://localhost:8000/health
```

## 🔧 **CONFIGURACIÓN AUTOMÁTICA**

El sistema detecta automáticamente:
- **Windows:** Usa configuración SSL permisiva
- **Mac/Linux:** Usa configuración SSL estándar

## ❌ **SI SIGUE FALLANDO EN WINDOWS:**

### **Opción A: Verificar firewall**
- Desactivar Windows Defender temporalmente
- Permitir Python en el firewall

### **Opción B: Actualizar certificados**
```bash
pip install --upgrade certifi
```

### **Opción C: Usar conexión directa**
Cambiar en `.env`:
```env
MONGO_URI=mongodb://barbdeveloper11_db_user:2sn26wQR1C4fQuoC@cluster0-shard-00-00.n7u5rn.mongodb.net:27017,cluster0-shard-00-01.n7u5rn.mongodb.net:27017,cluster0-shard-00-02.n7u5rn.mongodb.net:27017/ensemble_models?ssl=true&replicaSet=atlas-123456-shard-0&authSource=admin&retryWrites=true&w=majority
```

## 📞 **SOPORTE**

Si tienes problemas:
1. Ejecuta `python test_mongo_universal.py` y comparte el output
2. Verifica que la contraseña de MongoDB sea correcta
3. Verifica que tu IP esté en la whitelist de MongoDB Atlas
