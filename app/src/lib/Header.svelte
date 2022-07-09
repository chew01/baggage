<script>
    import {Hamburger} from "svelte-hamburgers";

    let logo = 'images/logo.png'
    let open
</script>

<header class="fixed w-full bg-[#e4dfc9] flex justify-between h-16 shadow-2xl z-20">
    <a href="/" class="flex justify-center items-center mx-4"><img src={logo} alt="Logo, link to main page" class="max-w-[200px]"/></a>
    <span class="sm:hidden z-30">
        <Hamburger bind:open/>
    </span>

    {#if open}
        <div class="fixed min-w-full sm:hidden z-20">
            <nav class="mt-16 flex flex-col">
                <a href="/auth" class="bg-[#ede7cc] h-16 flex justify-center items-center text-lg font-bold">Get
                    Started</a>
            </nav>
        </div>
    {/if}

    <nav class="hidden sm:flex flex-row items-center pr-8 gap-4">
        <a href="/auth" class="px-4 py-2 rounded-xl shadow-2xl flex justify-center items-center text-lg font-bold bg-yellow-100">Get started</a>
    </nav>
</header>
