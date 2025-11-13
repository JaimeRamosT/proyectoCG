#!/usr/bin/env node

/**
 * Script de verificación pre-despliegue para Vercel
 * Ejecutar: node check-vercel-ready.js
 */

import { readFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

console.log('🔍 Verificando configuración para Vercel...\n');

let allChecks = [];

// Check 1: Archivos requeridos
console.log('📁 Verificando archivos requeridos...');
const requiredFiles = [
  'vercel.json',
  '.env.example',
  '.env.production',
  'package.json',
  'vite.config.js',
  'src/config/api.js',
];

requiredFiles.forEach(file => {
  const exists = existsSync(join(__dirname, file));
  console.log(`  ${exists ? '✅' : '❌'} ${file}`);
  allChecks.push({ name: `Archivo ${file}`, passed: exists });
});

// Check 2: Configuración de Vercel
console.log('\n⚙️  Verificando vercel.json...');
try {
  const vercelConfig = JSON.parse(readFileSync(join(__dirname, 'vercel.json'), 'utf-8'));
  
  const hasRewrites = vercelConfig.rewrites && vercelConfig.rewrites.length > 0;
  console.log(`  ${hasRewrites ? '✅' : '❌'} Rewrites configurados (para SPA routing)`);
  allChecks.push({ name: 'Rewrites en vercel.json', passed: hasRewrites });
  
  const hasFramework = vercelConfig.framework === 'vite';
  console.log(`  ${hasFramework ? '✅' : '⚠️'} Framework: ${vercelConfig.framework || 'no especificado'}`);
  allChecks.push({ name: 'Framework configurado', passed: hasFramework });
} catch (error) {
  console.log('  ❌ Error leyendo vercel.json');
  allChecks.push({ name: 'vercel.json válido', passed: false });
}

// Check 3: Variables de entorno
console.log('\n🔐 Verificando variables de entorno...');
try {
  const envProd = readFileSync(join(__dirname, '.env.production'), 'utf-8');
  
  const hasApiUrl = envProd.includes('VITE_API_URL=');
  console.log(`  ${hasApiUrl ? '✅' : '❌'} VITE_API_URL definido`);
  allChecks.push({ name: 'VITE_API_URL en .env.production', passed: hasApiUrl });
  
  if (hasApiUrl) {
    const apiUrl = envProd.split('VITE_API_URL=')[1]?.split('\n')[0]?.trim();
    const isLocalhost = apiUrl?.includes('localhost');
    const hasUrl = apiUrl && apiUrl !== '';
    
    console.log(`  ${!isLocalhost && hasUrl ? '✅' : '⚠️'} URL: ${apiUrl || 'no definida'}`);
    if (isLocalhost) {
      console.log('  ⚠️  La URL apunta a localhost, actualízala para producción');
    }
    allChecks.push({ name: 'API URL no es localhost', passed: !isLocalhost && hasUrl });
  }
} catch (error) {
  console.log('  ❌ Error leyendo .env.production');
  allChecks.push({ name: '.env.production válido', passed: false });
}

// Check 4: package.json
console.log('\n📦 Verificando package.json...');
try {
  const pkg = JSON.parse(readFileSync(join(__dirname, 'package.json'), 'utf-8'));
  
  const hasBuildScript = pkg.scripts && pkg.scripts.build;
  console.log(`  ${hasBuildScript ? '✅' : '❌'} Script 'build': ${pkg.scripts?.build || 'no definido'}`);
  allChecks.push({ name: 'Script build en package.json', passed: hasBuildScript });
  
  const hasVite = pkg.devDependencies?.vite || pkg.dependencies?.vite;
  console.log(`  ${hasVite ? '✅' : '❌'} Vite instalado`);
  allChecks.push({ name: 'Vite en dependencias', passed: hasVite });
} catch (error) {
  console.log('  ❌ Error leyendo package.json');
  allChecks.push({ name: 'package.json válido', passed: false });
}

// Check 5: API config
console.log('\n🌐 Verificando configuración de API...');
try {
  const apiConfig = readFileSync(join(__dirname, 'src/config/api.js'), 'utf-8');
  
  const usesEnvVar = apiConfig.includes('import.meta.env.VITE_API_URL');
  console.log(`  ${usesEnvVar ? '✅' : '❌'} Usa variable de entorno VITE_API_URL`);
  allChecks.push({ name: 'API config usa env vars', passed: usesEnvVar });
  
  const hasProductionConfig = apiConfig.includes('production');
  console.log(`  ${hasProductionConfig ? '✅' : '❌'} Tiene configuración para producción`);
  allChecks.push({ name: 'Configuración de producción', passed: hasProductionConfig });
} catch (error) {
  console.log('  ❌ Error leyendo src/config/api.js');
  allChecks.push({ name: 'API config válido', passed: false });
}

// Check 6: Git
console.log('\n📝 Verificando Git...');
// Buscar .git en el directorio actual o en directorios padres (para monorepos)
let hasGit = existsSync(join(__dirname, '.git'));
if (!hasGit) {
  // Buscar en el directorio padre (común en monorepos)
  hasGit = existsSync(join(__dirname, '..', '.git'));
  if (!hasGit) {
    // Buscar dos niveles arriba
    hasGit = existsSync(join(__dirname, '..', '..', '.git'));
  }
}
console.log(`  ${hasGit ? '✅' : '⚠️'} Repositorio Git inicializado`);
allChecks.push({ name: 'Git inicializado', passed: hasGit });

if (hasGit) {
  console.log('  ℹ️  Asegúrate de hacer commit y push antes de desplegar');
} else {
  console.log('  ℹ️  Si estás en un monorepo, esto es normal');
}

// Resumen
console.log('\n' + '='.repeat(60));
console.log('📊 RESUMEN');
console.log('='.repeat(60));

const passed = allChecks.filter(c => c.passed).length;
const total = allChecks.length;
const percentage = Math.round((passed / total) * 100);

allChecks.forEach(check => {
  console.log(`${check.passed ? '✅' : '❌'} ${check.name}`);
});

console.log('='.repeat(60));
console.log(`\n${passed}/${total} verificaciones pasadas (${percentage}%)`);

if (percentage === 100) {
  console.log('\n✅ ¡Todo listo para desplegar en Vercel!');
  console.log('\n📚 Pasos siguientes:');
  console.log('  1. git add .');
  console.log('  2. git commit -m "Ready for Vercel deployment"');
  console.log('  3. git push origin main');
  console.log('  4. Ir a https://vercel.com/new y seguir las instrucciones');
  console.log('\n📖 Guía completa: DEPLOY_VERCEL.md');
} else if (percentage >= 70) {
  console.log('\n⚠️  Casi listo, pero hay algunas advertencias.');
  console.log('Revisa los elementos marcados con ⚠️ arriba.');
} else {
  console.log('\n❌ Hay problemas que deben ser resueltos antes de desplegar.');
  console.log('Revisa los elementos marcados con ❌ arriba.');
}

console.log('\n');
process.exit(percentage === 100 ? 0 : 1);
