<script>
let login = false;

async function onSubmitSignup(e) {
    const formData = new FormData(e.target);

    const signupRes = await fetch("http://192.46.228.205:8000/user/create",
        {method: "POST",
        mode: "no-cors",
        headers: {'Content-Type': 'application/json'},
        body: formData})
}

function onSubmitLogin(e) {
    const formData = new FormData(e.target);

    fetch("http://192.46.228.205:8000/user/login",
        {method: "POST",
            mode: "no-cors",
            headers: {'Content-Type': 'application/json'},
            body: formData}).then(console.log)
}

function toggleLoginStatus() {
    login = !login
}
</script>

<main class="relative min-h-screen bg-[url('/images/signup.jpg')] bg-cover bg-center flex flex-col justify-center">
    <div class="absolute left-0 top-0 min-h-full min-w-full bg-gray-500 opacity-60"></div>
    <div class="flex flex-col">
        <div class="flex flex-col items-center z-10">
            <h2 class="text-center text-4xl font-bold font-title text-[#f2edd8] sm:text-7xl">Almost there!</h2>
            {#if !login}
                <section class="bg-yellow-50 m-4 p-6 rounded-2xl">
                    <form class="flex flex-col gap-2" on:submit|preventDefault={onSubmitSignup}>
                        <div class="flex flex-col">
                            <label for="username" class="font-medium mb-1">Username</label>
                            <input name="username" id="username" class="border-2 rounded" required/>
                        </div>
                        <div class="flex flex-col">
                            <label for="password" class="font-medium mb-1">Password</label>
                            <input name="password" id="password" type="password" class="border-2 rounded" required/>
                        </div>
                        <div class="flex flex-col">
                            <label for="address" class="font-medium mb-1">Address</label>
                            <input name="address" id="address" class="border-2 rounded" required/>
                        </div>
                        <div class="flex flex-col">
                            <label for="postal_code" class="font-medium mb-1">Postal Code</label>
                            <input name="postal_code" id="postal_code" type="number" maxlength="6" minlength="6" class="border-2 rounded" required/>
                        </div>
                        <div class="flex flex-col">
                            <label for="unit_number" class="font-medium mb-1">Unit Number</label>
                            <input name="unit_number" id="unit_number" class="border-2 rounded" required/>
                        </div>

                        <button class="mt-4 mx-4 p-2 rounded-xl text-2xl font-bold bg-amber-100 border-2" type="submit">Sign up</button>
                    </form>
                    <p class="mt-4 font-medium italic">Have an account? Click <button on:click={toggleLoginStatus} class="text-blue-800 underline">here</button> to login instead</p>
                </section>
            {:else }
                <section class="bg-yellow-50 m-4 p-6 rounded-2xl">
                    <form class="flex flex-col gap-2" on:submit|preventDefault={onSubmitLogin}>
                        <div class="flex flex-col">
                            <label for="loginUsername" class="font-medium mb-1">Username</label>
                            <input name="username" id="loginUsername" class="border-2 rounded" required/>
                        </div>
                        <div class="flex flex-col">
                            <label for="loginPassword" class="font-medium mb-1">Password</label>
                            <input name="password" id="loginPassword" type="password" class="border-2 rounded" required/>
                        </div>
                        <button class="mt-4 mx-4 p-2 rounded-xl text-2xl font-bold bg-amber-100 border-2" type="submit">Log in</button>
                    </form>
                    <p class="mt-4 font-medium italic">Click <button on:click={toggleLoginStatus} class="text-blue-800 underline">here</button> to sign up instead</p>
                </section>
            {/if}
        </div>
    </div>
</main>
