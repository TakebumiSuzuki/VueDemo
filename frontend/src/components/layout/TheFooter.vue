<script setup>
    import ContactForm from '@components/sections/ContactForm.vue';
</script>

<template>

    <div class="py-8 bg-zinc-800 text-zinc-100">
        <div class="max-w-[1200px] mx-auto px-16 ">
            <h2 class="text-5xl font-medium text-center pt-12 pb-10">CONTACT</h2>

            <div class="md:flex md:flex-row md:justify-center md:items-start md:gap-16 mt-6">
                <div class="space-y-6 md:w-1/2 w-full mt-4 max-md:mb-16">
                    <p>テキストテキストテキスト</p>
                    <p>テキストテキストテキストテキストテキストテキストテキストテキストテキスト テキストテキストテキストテキストテキストテキストテキストテキストテキスト テキストテキストテキストテキストテキストテキストテキストテキストテキスト</p>
                    <p>テキストテキストテキストテキストテキストテキストテキストテキストテキスト テキストテキストテキストテキストテキストテキストテキストテキストテキストテキスト テキストテキストテキストテキストテキストテキストテキストテキストテキスト</p>
                </div>

                <ContactForm />
            </div>

            <small class="text-white text-xs mt-16 block text-center mx-auto">
                © Sneakers
            </small>
        </div>
    </div>

</template>