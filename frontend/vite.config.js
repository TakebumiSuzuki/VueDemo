import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import { fileURLToPath, URL } from 'node:url'

// https://vite.dev/config/
export default defineConfig({

  plugins: [vue(), tailwindcss(),],

  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      '@components': fileURLToPath(new URL('./src/components', import.meta.url))
    }
  },
  server: {
    proxy: {
      // 文字列 '/api' で始まるリクエストをターゲットに転送する
      '/api': {
        target: 'http://localhost:5000', // あなたのAPIサーバーのアドレス
        changeOrigin: true, // オリジンヘッダーを変更（CORS対策で重要）
        // オプション: パスを書き換える場合
        // rewrite: (path) => path.replace(/^\/api/, '') // '/api/contact' -> '/contact'
      },
    }
  },
  build: {
    outDir: '../backend/static',  // Flaskのstaticフォルダに直接出力
    emptyOutDir: true,
    rollupOptions: {
      output: {
        // アセットファイルの命名規則を調整
        assetFileNames: 'assets/[name]-[hash][extname]',
        chunkFileNames: 'assets/[name]-[hash].js',
        entryFileNames: 'assets/[name]-[hash].js'
      }
    }
  },
  base: '/',
})
