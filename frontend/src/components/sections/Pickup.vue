<script setup>
    import 'vue3-carousel/dist/carousel.css'
    import { Carousel, Slide, Pagination, Navigation } from 'vue3-carousel'

    let slides = []
    for (let i=1; i<=9; i++) {
        //importのくだりは、viteのビルドプロセスで、'/static/'のパスをつけてくれる様にするため。
        slides.push(`/img/pickup${i}.jpg`)
    }

</script>

<template>
    <carousel :items-to-show="3.5" :wrap-around="true">

        <slide v-for="slide in slides" :key="slide">
            <div class="carousel__item" >
                <img :src="slide" alt="" class="w-[80%]">
            </div>
        </slide>

        <template #addons>
            <navigation />
        </template>

    </carousel>

</template>