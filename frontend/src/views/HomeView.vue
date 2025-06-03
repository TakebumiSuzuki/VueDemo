<script setup>
    import TheHero from '@components/layout/TheHero.vue';
    import SectionTitle from '@/components/ui/SectionTitle .vue';
    import PickUp from '@components/sections/Pickup.vue';
    import Feature from '@components/sections/Feature.vue';



</script>


<template>
    <TheHero class=""/>

    <section id="pick-up" class="mt-14">
        <SectionTitle text="PICK UP" />
        
        <PickUp/>
    </section>


    <section id="feature" class="mt-14">
        <SectionTitle text="FEATURE" />
        <Feature />
    </section>

</template>