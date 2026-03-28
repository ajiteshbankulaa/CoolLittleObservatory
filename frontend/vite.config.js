import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { viteStaticCopy } from "vite-plugin-static-copy";
export default defineConfig({
    plugins: [
        react(),
        viteStaticCopy({
            targets: [
                {
                    src: "node_modules/cesium/Build/Cesium/*",
                    dest: "cesium",
                },
            ],
        }),
    ],
    resolve: {
        alias: {
            "@": "/src",
        },
    },
    define: {
        CESIUM_BASE_URL: JSON.stringify("/cesium"),
    },
    build: {
        rollupOptions: {
            output: {
                manualChunks: {
                    cesium: ["cesium"],
                    react: ["react", "react-dom"],
                    query: ["@tanstack/react-query"],
                },
            },
        },
    },
    server: {
        port: 5173,
    },
});
