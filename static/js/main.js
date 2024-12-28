document.addEventListener("DOMContentLoaded", () => {
    // Toast element
    const toast = document.getElementById("basket-toast");
    const toastBody = toast.querySelector(".toast-body");

    // Function to update basket count and preview
    const updateBasketPreview = () => {
        fetch("/basket/")
            .then((response) => response.text())
            .then((html) => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, "text/html");
                const basketPreview = doc.querySelector("#basket-content").innerHTML;
                document.getElementById("basket-content").innerHTML = basketPreview;
                document.getElementById("basket-count").innerText = doc.querySelector("#basket-count").innerText;
            });
    };

    // AJAX handler for "Add to Basket"
    document.querySelectorAll(".add-to-basket").forEach((button) => {
        button.addEventListener("click", (e) => {
            e.preventDefault();
            const url = button.getAttribute("href");
            fetch(url, { headers: { "X-Requested-With": "XMLHttpRequest" } })
                .then((response) => response.json())
                .then((data) => {
                    toastBody.textContent = data.message;
                    const bootstrapToast = new bootstrap.Toast(toast);
                    bootstrapToast.show();
                    document.getElementById("basket-count").innerText = data.basket_count;
                });
        });
    });

    // Hover to load basket preview
    const basketPreview = document.getElementById("basket-preview");
    basketPreview.addEventListener("mouseover", updateBasketPreview);
});