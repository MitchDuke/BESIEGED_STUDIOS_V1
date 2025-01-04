document.addEventListener("DOMContentLoaded", () => {
    // Function to update basket preview
    const updateBasketPreview = () => {
        fetch("/basket/", { headers: { "X-Requested-With": "XMLHttpRequest" } })
            .then((response) => response.text())
            .then((html) => {
                document.getElementById("basket-content").innerHTML = html;
            });
    };

    // Update basket count when adding items
    const toast = document.getElementById("basket-toast");
    const toastBody = toast.querySelector(".toast-body");
    document.querySelectorAll(".add-to-basket-form").forEach((form) => {
        form.addEventListener("submit", (e) => {
            e.preventDefault();

            const url = form.getAttribute("action");
            const csrfToken = form.querySelector("input[name=csrfmiddlewaretoken]").value;

            fetch(url, {
                method: "POST",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": csrfToken,
                },
            })
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