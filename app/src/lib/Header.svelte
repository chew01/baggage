<script>
    import {Hamburger} from "svelte-hamburgers";

    let open
</script>

<header class="bg-gray-300 flex justify-between h-16">
    <a href="/">Logo goes here</a>
    <span class="sm:hidden z-30">
        <Hamburger bind:open/>
    </span>

    {#if open}
        <div class="fixed min-w-full sm:hidden">
            <nav class="mt-16 flex flex-col">
                <a href="/about" class="bg-gray-100 h-16 flex justify-center items-center border-b-2 text-lg font-bold">About</a>
                <a href="/login" class="bg-gray-100 h-16 flex justify-center items-center border-b-2 text-lg font-bold">Get
                    Started</a>
            </nav>
        </div>
    {/if}

    <nav class="hidden sm:flex flex-row pr-8 gap-4">
        <a href="/about" class="flex justify-center items-center text-lg font-bold">About page</a>
        <a href="/login" class="flex justify-center items-center text-lg font-bold">Get started</a>
    </nav>

</header>
