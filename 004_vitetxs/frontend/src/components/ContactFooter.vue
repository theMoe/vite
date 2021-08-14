<template>
    <footer>
        <div class="seperator"/>
        <div class="contact">
            <p><i class="fas fa-bug"/> <em>contact or bug report:</em></p>
            <a href="https://twitter.com/vitetools" target="_blank"
            ><i class="fab fa-twitter"/>
            </a>
        </div>
        <div class="support">
            <p><i class="fas fa-mug-hot"/> <em>support for our work:</em></p>
            <p class="address">vite_a47eae663ea3a90ffe9651e2855cc8c7fe90456104e281f3d1</p>
            <img src="../assets/viteTxsDonationAddress.png"/>
        </div>
    </footer>
</template>

<style scoped>
footer {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    margin: 50px 0 0; 
    font-size: 16px;
}

footer em {
    font-style: normal;
    letter-spacing: 0.1em;
    font-weight: bold;
    margin-left: 5px;
}

.seperator {
    width: 100%;
    height: 1px;
    border-radius: 5px;
    margin-bottom: 15px;
    background: var(--blue-lightest);
}

.contact {
    display: flex;
}

.contact p {
    margin: 0 10px 0 0;
}

.contact .fa-twitter {
    font-size: 24px !important;
}

.support {
    display: flex;
    align-items: center;
    flex-direction: column;
    margin: 15px 0 0;
}

.support p:last-of-type {
    margin-top: 10px;
    color: var(--blue-darkest);
    background: linear-gradient(-45deg, var(--blue-dark), var(--orange-dark));
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.support img {
    width: 100px;
    margin-top: 10px;
}

@media (max-width: 1000px) {
    footer {
        background: white;
        border-radius: 25px;
        padding: 15px 5px 10px;
        border-radius: 25px;
        background: white;
        background: linear-gradient(270deg, #fef9f6 0%, #f6fafe 100%);
        box-shadow: 6px 6px 15px rgba(0, 0, 0, 0.3);
        flex-basis: 90%;
    }

    .seperator {
        display: none;
    }
}

@media (max-width: 500px) {
    footer {
        flex-basis: 100%;
    }

    footer .address {
        word-break: break-all;
        padding: 0px 15px;
    }
}
</style>