// This is your test publishable API key.
const stripe = Stripe("pk_live_51MyeVkHDR3k1aZOHkBfRpVmtiyS1aH1HGj9zqMy9h1P62ZEVyD6cZfi6cDrWT2YJw5opTUQJKKxgBAi87CjVu1NR00gW6uZ8Qs");

// The items the customer wants to buy
const items = [{ id: "xl-tshirt" }];

let elements;
let carousel = null;
let emailAddress = '';

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

function next_slice() {
    carousel.next();
}

async function create_order() {
    let t_size = document.querySelector("input[name='size_options']:checked").value;
    let t_quantity = document.querySelector("input[name='quantity_options']:checked").value;
    let t_area = document.querySelector("input[name='area_options']:checked").value;
    let t_name = document.querySelector("input[name='name']").value;
    let t_mobile = document.querySelector("input[name='mobile']").value;
    let t_address = document.querySelector("textarea[name='address']").value;
    let t_notes = document.querySelector("textarea[name='notes']").value;
    let csrf = document.querySelector("input[name='csrfmiddlewaretoken']").value;

    const request_data = new FormData();
    request_data.append('t_size', t_size);
    request_data.append('t_quantity', t_quantity);
    request_data.append('t_area', t_area);
    request_data.append('t_name', t_name);
    request_data.append('t_mobile', t_mobile);
    request_data.append('t_address', t_address);
    request_data.append('t_notes', t_notes);
    request_data.append('csrfmiddlewaretoken', csrf);

    const response = await fetch("/yangmei_intent/", {
        method: "POST",
        body: request_data,
    });

    const { clientSecret } = await response.json();
    const appearance = {
        theme: 'stripe',
    };
    const paymentElementOptions = {
        layout: "tabs",
    };
    elements = stripe.elements({ appearance, clientSecret });
    const paymentElement = elements.create("payment", paymentElementOptions);
    paymentElement.mount("#payment-element");
}

function yangmei_init() {
    carousel = new bootstrap.Carousel('#myCarousel');

    document.querySelector("#payment-form").addEventListener("submit", handleSubmit);
    document.querySelectorAll("label[name='size']").forEach(e => {
        e.addEventListener(
            'click',
            e => {
                next_slice();
            });
    });
    document.querySelectorAll("label[name='quantity']").forEach(e => {
        e.addEventListener(
            'click',
            e => {
                next_slice();
            });
    });
    document.querySelectorAll("label[name='area']").forEach(e => {
        e.addEventListener(
            'click',
            e => {
                next_slice();
            });
    });
    document.querySelector("div[name='order_button']").addEventListener('click', e => {
        create_order();
    });
    checkStatus();
}

$(document).ready(function () {
    yangmei_init();
})