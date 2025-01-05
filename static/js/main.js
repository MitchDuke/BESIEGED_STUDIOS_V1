document.addEventListener("DOMContentLoaded", () => {
    // Function to update the basket dropdown and count
    const updateBasketPreview = () => {
        const basketContent = document.getElementById("basket-content");
        const basketCount = document.getElementById("basket-count");

        fetch("/basket/", { headers: { "X-Requested-With": "XMLHttpRequest" } })
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.text();
            })
            .then((html) => {
                basketContent.innerHTML = html; // Update dropdown content

                // Update basket count
                const itemCount = basketContent.querySelectorAll("li").length;
                basketCount.textContent = itemCount > 0 ? itemCount : 0;
            })
            .catch((error) => {
                console.error("Error updating basket preview:", error);
            });
    };

    // Handle adding items to the basket
    const toast = document.getElementById("basket-toast");
    const toastBody = toast?.querySelector(".toast-body");

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
                .then((response) => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then((data) => {
                    if (toastBody) {
                        toastBody.textContent = data.message; // Show success message
                        const bootstrapToast = new bootstrap.Toast(toast);
                        bootstrapToast.show();
                    }

                    // Update basket count and refresh dropdown
                    document.getElementById("basket-count").innerText = data.basket_count;
                    updateBasketPreview();
                })
                .catch((error) => {
                    console.error("Error adding to basket:", error);
                });
        });
    });

    // Hover to trigger basket preview update
    const basketPreview = document.getElementById("basket-preview");
    basketPreview?.addEventListener("mouseover", updateBasketPreview);
});