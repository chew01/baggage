<script>
    import {onMount} from "svelte";

    let upcoming = [];
    let listings = [];

    onMount(async () => {
        // Currently require endpoints to find listings accepted and listings posted by user
    })
</script>

<main class="bg-amber-50 min-h-screen p-2 pt-6 flex flex-col gap-6">
    <h1 class="font-bold text-5xl text-center mb-4 sm:text-left sm:pl-6">Dashboard</h1>
    <section>
        <h2 class="font-medium text-2xl text-center sm:text-left sm:pl-6">Your upcoming collections</h2>
        {#if upcoming.length === 0}
            <article class="m-4 p-6 bg-gray-200 rounded-xl flex items-center gap-2 shadow-xl sm:w-[400px] sm:h-[300px]">
                <p class="font-medium text-xl">You have no upcoming collections.<br/>Check out the <a href="/market" class="text-blue-800">Market</a>!</p>
            </article>
        {/if}
    </section>
    <section>
        <h2 class="font-medium text-2xl text-center sm:text-left sm:pl-6">Your listings</h2>
        {#if listings.length === 0}
            <article class="m-4 p-6 bg-gray-200 rounded-xl flex items-center gap-2 shadow-xl sm:w-[400px] sm:h-[300px] ">
                <p class="font-medium text-xl">You have no ongoing listings. <br/> Create one <a href="/listing/create" class="text-blue-800">here</a>!</p>
            </article>
        {/if}
    </section>
</main>
