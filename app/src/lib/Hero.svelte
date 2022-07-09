<script>

import Minimized from "./Minimized.svelte";

</script>

<section class="relative min-h-screen bg-amber-50 bg-[url('/images/hero.jpg')] bg-cover bg-center flex flex-col justify-center">
    <div class="absolute left-0 top-0 min-h-full min-w-full bg-gray-500 opacity-60"></div>
        <div class="flex flex-col justify-center">
            <div class="py-4 flex flex-col z-10 gap-4 mb-4 lg:flex-row lg:justify-center xl:gap-16 2xl:gap-24">
                <div class="flex flex-col justify-center items-center">
                    <h2 class="text-center text-4xl font-bold font-title text-[#f2edd8] lg:text-7xl">Share a meal.</h2>
                    <h2 class="text-center text-3xl font-bold font-title text-[#f2edd8] lg:text-6xl">Make a difference.</h2>
                    <h2 class="mt-8 text-center text-3xl font-bold font-title text-[#f2edd8] max-w-lg lg:text-4xl">You're a step away from making someone's day.</h2>
                </div>
                <div class="flex flex-col items-center">
                    <Minimized title="Cucumbers" description="A bunch of cucumbers ready to eat" imageSrc="images/demo_cucumber.jpg" address="Bukit Batok" expiry="15 July 2022"/>
                    <a href="/auth" class="px-10 py-2 bg-yellow-100 rounded-xl font-bold text-xl shadow-2xl">Get started</a>
                </div>
            </div>
        </div>
</section>
