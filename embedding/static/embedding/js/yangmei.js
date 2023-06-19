// This is your test publishable API key.
const stripe = Stripe("pk_live_51MyeVkHDR3k1aZOHkBfRpVmtiyS1aH1HGj9zqMy9h1P62ZEVyD6cZfi6cDrWT2YJw5opTUQJKKxgBAi87CjVu1NR00gW6uZ8Qs");

// The items the customer wants to buy
const items = [{ id: "xl-tshirt" }];

let elements;
let carousel = null;
let emailAddress = '';

// Fetches a payment intent and captures the client secret
async function initialize() {
    const response = await fetch("/yangmei_intent/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ items }),
    });
    const { clientSecret } = await response.json();

    const appearance = {
        theme: 'stripe',
    };
    elements = stripe.elements({ appearance, clientSecret });

    const paymentElementOptions = {
        layout: "tabs",
    };

    const paymentElement = elements.create("payment", paymentElementOptions);
    paymentElement.mount("#payment-element");
}

async function handleSubmit(e) {
    e.preventDefault();
    const { error } = await stripe.confirmPayment({
        elements,
        confirmParams: {
            // Make sure to change this to your payment completion page
            return_url: "https://www.asuperdomain.com/pay_success/",
            receipt_email: 'zhuminjun01@gmail.com',
        },
    });

    // This point will only be reached if there is an immediate error when
    // confirming the payment. Otherwise, your customer will be redirected to
    // your `return_url`. For some payment methods like iDEAL, your customer will
    // be redirected to an intermediate site first to authorize the payment, then
    // redirected to the `return_url`.
    if (error.type === "card_error" || error.type === "validation_error") {
        showMessage(error.message);
    } else {
        showMessage("An unexpected error occurred.");
    }
}

// Fetches the payment intent status after payment submission
async function checkStatus() {
    const clientSecret = new URLSearchParams(window.location.search).get(
        "payment_intent_client_secret"
    );

    if (!clientSecret) {
        return;
    }

    const { paymentIntent } = await stripe.retrievePaymentIntent(clientSecret);

    switch (paymentIntent.status) {
        case "succeeded":
            showMessage("Payment succeeded!");
            break;
        case "processing":
            showMessage("Your payment is processing.");
            break;
        case "requires_payment_method":
            showMessage("Your payment was not successful, please try again.");
            break;
        default:
            showMessage("Something went wrong.");
            break;
    }
}

// ------- UI helpers -------

function showMessage(messageText) {
    const messageContainer = document.querySelector("#payment-message");

    messageContainer.classList.remove("hidden");
    messageContainer.textContent = messageText;

    setTimeout(function () {
        messageContainer.classList.add("hidden");
        messageContainer.textContent = "";
    }, 4000);
}

function next_entrance(index) {
    carousel.next();
}

function yangmei_init() {
    carousel = new bootstrap.Carousel('#myCarousel');

    document.querySelector("#payment-form").addEventListener("submit", handleSubmit);
    document.querySelectorAll("label[name='size']").forEach(e => {
        e.addEventListener(
            'click',
            e => {
                next_entrance(1);
            });
    });
    document.querySelectorAll("label[name='quantity']").forEach(e => {
        e.addEventListener(
            'click',
            e => {
                next_entrance(2);
            });
    });
    document.querySelectorAll("label[name='area']").forEach(e => {
        e.addEventListener(
            'click',
            e => {
                next_entrance(3);
            });
    });
    document.querySelector("div[name='order_button']").addEventListener('click', e => {
        next_entrance(4);
    });
    // document.querySelector("button[name='order']").addEventListener(e => {
    //     next_entrance(4);
    // });
    // document.querySelector("button[name='pay']").addEventListener(e => {
    //     next_entrance(5);
    // });
    initialize();
    checkStatus();
}

$(document).ready(function () {
    yangmei_init();
})