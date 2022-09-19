// Get Stripe publishable key
fetch("/config")
    .then((result) => {
        return result.json();
    })
    .then((data) => {
        // Initialize Stripe.js
        const stripe = Stripe(data.publicKey);

        // get item id
        const item_id = JSON.parse(document.getElementById('item-id').textContent);

        // Event handler
        document.querySelector("#submitBtn").addEventListener("click", () => {
            // Get Checkout Session ID
            fetch("/buy/" + item_id)
                .then((result) => {
                    return result.json();
                })
                .then((data) => {
                    console.log(data);
                    // Redirect to Stripe Checkout
                    return stripe.confirmCardPayment(data.client_secret, {
                        payment_method: {
                            cardNumber: 4242424242424242,
                            billing_details: {
                                name: "John Henry"
                            }

                        }
                    });
                })
                .then((res) => {
                    console.log(res);
                }).catch((err) => {
                    console.log(err)
                });
        });
    });