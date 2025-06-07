document.addEventListener("DOMContentLoaded", function () {
    const CATEGORY_OPTIONS = {
        single_mini: [
            { value: "small_hero", label: "Small Hero" },
            { value: "monster", label: "Monster" },
            { value: "tank", label: "Tank/Walker" },
        ],
        squad: [
            { value: "1_5", label: "Up to 5 Men" },
            { value: "6_10", label: "6 to 10 Men" },
            { value: "11_15", label: "11 to 15 Men" },
            { value: "16_20", label: "16 to 20 Men" },
            { value: "21_plus", label: "21+ Men (Case by Case)" },
        ],
        colossal: [
            { value: "colossal_monster", label: "Colossal Monster" },
            { value: "colossal_vehicle", label: "Colossal Vehicle" },
            { value: "over_20cm", label: "Over 20cm (Case by Case)" },
        ],
        terrain: [
            { value: "10cm", label: "≤ 10cm Combined" },
            { value: "20cm", label: "≤ 20cm Combined" },
            { value: "40cm", label: "≤ 40cm Combined" },
            { value: "50cm", label: "> 50cm Combined (Case by Case)" },
        ]
    };

    const categorySelect = document.getElementById("id_category");
    const sizeOptionSelect = document.getElementById("id_size_option");

    if (!categorySelect || !sizeOptionSelect) return;

    categorySelect.addEventListener("change", () => {
        const selectedCategory = categorySelect.value;
        const options = CATEGORY_OPTIONS[selectedCategory] || [];

        // Clear existing
        sizeOptionSelect.innerHTML = "";

        // Add placeholder
        const placeholder = document.createElement("option");
        placeholder.text = "--- Select Size ---";
        placeholder.value = "";
        sizeOptionSelect.appendChild(placeholder);

        // Add category-specific options
        options.forEach(option => {
            const opt = document.createElement("option");
            opt.value = option.value;
            opt.text = option.label;
            sizeOptionSelect.appendChild(opt);
        });
    });
});
