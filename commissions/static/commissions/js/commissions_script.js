document.addEventListener("DOMContentLoaded", function () {
    const CATEGORY_OPTIONS = {
        single_mini: [
            { value: "small_hero", label: "Small Hero (+10%)" },
            { value: "monster", label: "Monster (+10%)" },
            { value: "tank", label: "Tank/Walker (+15%)" },
        ],
        squad: [
            { value: "0_5", label: "0 to 5 Men (+10%)" },
            { value: "6_10", label: "6 to 10 Men (+10%)" },
            { value: "11_15", label: "11 to 15 Men (+10%)" },
            { value: "16_20", label: "16 to 20 Men (+15%)" },
            { value: "21_plus", label: "21+ Men (Case by Case)" },
        ],
        colossal: [
            { value: "colossal_monster", label: "Colossal Monster (+20%)" },
            { value: "colossal_vehicle", label: "Colossal Vehicle (+20%)" },
            { value: "over_20cm", label: "Over 20cm (Case by Case)" },
        ],
        terrain: [
            { value: "10cm", label: "≤ 10cm Combined (+10%)" },
            { value: "20cm", label: "≤ 20cm Combined (+15%)" },
            { value: "40cm", label: "≤ 40cm Combined (+20%)" },
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
