<script setup>
    import { ref, onMounted } from 'vue';
    import { useRouter, useRoute } from 'vue-router';
    import axios from 'axios';

    import SectionTitle from '@/components/ui/SectionTitle .vue';
    import Button from '@/components/ui/Button.vue';
    import Spinner from '@/components/ui/Spinner.vue';

    const route = useRoute();
    const router = useRouter();

    const productId = ref(null)

    const product = ref(null);
    const isLoading = ref(true);
    const error = ref(null);

    onMounted( async () => {
        const id = route.params.productId;
        if (!id) {
            error.value = "Product ID was not found in the url.";
            isLoading.value = false;
            return;
        }
        productId.value = id;

        try {
            const response = await axios.get(`/api/item/${productId.value}`);
            product.value = response.data;

        } catch (err) {
            console.error("Failed to fetch product details:", err);
            error.value = "Failed to obtain the product data. Please try later again.";

        } finally {
            isLoading.value = false;
        }
    });

    const goHome = () => {
        router.push({ name: 'Home' });
    }

    const goEditProduct = () => {
        router.push({ name: 'EditProduct' })
    }


</script>

<template>
    <div class="max-w-[1200px] mx-auto px-16 pb-20">
        <SectionTitle text="Item Info" />

        <div v-if="isLoading" class="min-h-[40vh] flex justify-center">
            <Spinner class="animate-spin size-12 text-gray-400 " />
        </div>

        <div v-else-if="error">
            <p class="min-h-[40vh] text-center text-xl text-red-500 pt-10">
                {{ error }}
            </p>
            <Button loadingText="Processing" text="Go Home" :isLoading="isLoading"
                    class="bg-gradient-to-br from-indigo-500 to-indigo-700 opacity-90 hover:opacity-100 mx-auto"
                    @click="goHome"
            />
        </div>

        <div v-else-if="product">
            <div class="flex flex-col md:flex-row items-start justify-center gap-8 md:gap-10
                text-zinc-800 dark:text-zinc-100">
                <div class="w-full md:w-1/2">
                    <img :src="product.image_url" :alt="product.name" >
                </div>
                <div class="w-full md:w-1/2">
                    <div>{{ product.category }}</div>
                    <h2 class="md:text-4xl text-3xl mt-2">{{ product.name }}</h2>
                    <p class="text-lg leading-tight mt-8">{{ product.description }}</p>
                    <p class="mt-12 text-base">Price: ${{ product.price }}</p>
                </div>
            </div>

            <div class="flex md:flex-row flex-col md:justify-center items-center md:gap-10 gap-4 pt-24">
                <Button loadingText="Processing" text="Go Back Home" :isLoading="isLoading"
                    class="bg-gradient-to-br from-indigo-500 to-indigo-700 opacity-90 hover:opacity-100"
                    @click="goHome"
                />
                <Button loadingText="Processing" text="Edit Item (Admin Mode)" :isLoading="isLoading"
                    class="bg-gradient-to-br from-pink-500 to-pink-700 opacity-90 hover:opacity-100"
                    @click="goEditProduct"
                />
            </div>
        </div>

        <div v-else>
            <p class="min-h-screen flex justify-center items-center text-xl">
                Couldn't faind the product.
            </p>
        </div>

    </div>

</template>