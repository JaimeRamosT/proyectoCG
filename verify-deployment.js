#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

console.log('🔍 Verificando configuración para Vercel...\n');

const checks = [];

// 1. Verificar vercel.json
const vercelJsonPath = path.join(__dirname, 'vercel.json');
if (fs.existsSync(vercelJsonPath)) {
  checks.push({ name: 'vercel.json existe', status: true });
  
  const config = JSON.parse(fs.readFileSync(vercelJsonPath, 'utf-8'));
  checks.push({ 
    name: 'Configuración de builds', 
    status: config.builds && config.builds.length === 2 
  });
  checks.push({ 
    name: 'Configuración de routes', 
    status: config.routes && config.routes.length >= 2 
  });
  checks.push({ 
    name: 'Configuración de functions', 
    status: config.functions && config.functions['api/index.py'] 
  });
} else {
  checks.push({ name: 'vercel.json existe', status: false });
}

// 2. Verificar api/index.py
const apiIndexPath = path.join(__dirname, 'api', 'index.py');
checks.push({ 
  name: 'api/index.py existe', 
  status: fs.existsSync(apiIndexPath) 
});

// 3. Verificar api/requirements.txt
const requirementsPath = path.join(__dirname, 'api', 'requirements.txt');
checks.push({ 
  name: 'api/requirements.txt existe', 
  status: fs.existsSync(requirementsPath) 
});

// 4. Verificar modelo AOT-GAN
const modelPath = path.join(__dirname, 'api', 'setup', 'experiments', 'CELEBA-HQ', 'G0000000.pt');
if (fs.existsSync(modelPath)) {
  const stats = fs.statSync(modelPath);
  const sizeMB = (stats.size / (1024 * 1024)).toFixed(2);
  checks.push({ 
    name: `Modelo G0000000.pt (${sizeMB} MB)`, 
    status: stats.size > 50 * 1024 * 1024 // > 50MB
  });
} else {
  checks.push({ name: 'Modelo G0000000.pt', status: false });
}

// 5. Verificar api/src/aot_inpainting.py
const aotInpaintingPath = path.join(__dirname, 'api', 'src', 'aot_inpainting.py');
checks.push({ 
  name: 'api/src/aot_inpainting.py existe', 
  status: fs.existsSync(aotInpaintingPath) 
});

// 6. Verificar frontend build
const distPath = path.join(__dirname, 'image_inpainting_web', 'dist');
checks.push({ 
  name: 'Frontend build (dist) existe', 
  status: fs.existsSync(distPath) 
});

// 7. Verificar frontend package.json
const frontendPackageJsonPath = path.join(__dirname, 'image_inpainting_web', 'package.json');
if (fs.existsSync(frontendPackageJsonPath)) {
  const packageJson = JSON.parse(fs.readFileSync(frontendPackageJsonPath, 'utf-8'));
  checks.push({ 
    name: 'Script vercel-build en package.json', 
    status: packageJson.scripts && packageJson.scripts['vercel-build'] 
  });
} else {
  checks.push({ name: 'Frontend package.json', status: false });
}

// 8. Verificar .vercelignore
const vercelIgnorePath = path.join(__dirname, '.vercelignore');
checks.push({ 
  name: '.vercelignore existe', 
  status: fs.existsSync(vercelIgnorePath) 
});

// 9. Verificar config API en frontend
const apiConfigPath = path.join(__dirname, 'image_inpainting_web', 'src', 'config', 'api.js');
checks.push({ 
  name: 'Frontend API config existe', 
  status: fs.existsSync(apiConfigPath) 
});

// Mostrar resultados
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
checks.forEach(check => {
  const icon = check.status ? '✅' : '❌';
  console.log(`${icon} ${check.name}`);
});
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

const allPassed = checks.every(check => check.status);
if (allPassed) {
  console.log('✨ Todo listo para deployment en Vercel!');
  console.log('\nPasos siguientes:');
  console.log('1. Ejecuta: vercel --prod');
  console.log('2. O haz push a tu repositorio conectado a Vercel\n');
  process.exit(0);
} else {
  console.log('⚠️  Hay problemas que necesitan ser resueltos antes del deployment.\n');
  process.exit(1);
}
