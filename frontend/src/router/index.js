import { createRouter, createWebHistory } from 'vue-router';

import HomeView from '@/views/HomeView.vue';
import ProductView from '@/views/ProductView.vue';
import CreateProductView from '@/views/CreateProductView.vue';
import EditProductView from '@/views/EditProductView.vue';


const routes = [
    {
        path: '/',
        name: 'Home',
        component: HomeView
    },
    {
        path: '/product/:productId',
        name: 'Product',
        component: ProductView,
    },
    {
        path: '/admin/product/:productId/edit',
        name: 'EditProduct',
        component: EditProductView,
    },
    {
        path: '/admin/create-item',
        name: 'CreateProduct',
        component: CreateProductView,
    }
];

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes, // `routes: routes` の省略形
    scrollBehavior(to, from, savedPosition) {
        return new Promise((resolve) => {
            // 少し遅延させてからスクロールを実行
            setTimeout(() => {
                if (savedPosition) {
                    resolve(savedPosition);
                } else if (to.hash) {
                    resolve({
                        el: to.hash,
                        behavior: 'smooth',
                    });
                } else {
                    resolve({ left: 0, top: 0 });
                }
            }, 100); // 100ms の遅延
        });
    }
});

export default router;