document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("search-input");
  const categoryBtns = document.querySelectorAll(".btn-category");
  const sortSelect = document.getElementById("sort-select");
  const gridContainer = document.getElementById("business-grid");

  let cards = Array.from(document.querySelectorAll(".card"));

  let activeCategory = "todos";

  /* =========================================
     FILTRAR TARJETAS
  ========================================= */

  function filterCards() {
    const query = searchInput.value.toLowerCase().trim();

    cards.forEach((card) => {
      const title = card.getAttribute("data-title")?.toLowerCase() || "";

      const category = card.getAttribute("data-category") || "";

      const description =
        card.querySelector(".card-content p")?.textContent.toLowerCase() || "";

      const matchesSearch =
        title.includes(query) || description.includes(query);

      const matchesCategory =
        activeCategory === "todos" || category === activeCategory;

      if (matchesSearch && matchesCategory) {
        card.style.display = "flex";
      } else {
        card.style.display = "none";
      }
    });
  }

  /* =========================================
     BUSCADOR
  ========================================= */

  searchInput.addEventListener("input", filterCards);

  /* =========================================
     CATEGORÍAS
  ========================================= */

  categoryBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      categoryBtns.forEach((button) => {
        button.classList.remove("active");
      });

      btn.classList.add("active");

      activeCategory = btn.getAttribute("data-category");

      filterCards();
    });
  });

  /* =========================================
     ORDENAMIENTO
  ========================================= */

  sortSelect.addEventListener("change", () => {
    const order = sortSelect.value;

    let sortedCards = [...cards];

    if (order === "asc") {
      sortedCards.sort((a, b) => {
        const titleA = a.getAttribute("data-title") || "";

        const titleB = b.getAttribute("data-title") || "";

        return titleA.localeCompare(titleB, "es", {
          sensitivity: "base",
        });
      });
    } else if (order === "desc") {
      sortedCards.sort((a, b) => {
        const titleA = a.getAttribute("data-title") || "";

        const titleB = b.getAttribute("data-title") || "";

        return titleB.localeCompare(titleA, "es", {
          sensitivity: "base",
        });
      });
    } else if (order === "aleatorio") {
      sortedCards.sort(() => Math.random() - 0.5);
    }

    /* Volver a colocar las tarjetas */

    gridContainer.innerHTML = "";

    sortedCards.forEach((card) => {
      gridContainer.appendChild(card);
    });

    /* Actualizar referencia */

    cards = Array.from(gridContainer.querySelectorAll(".card"));

    filterCards();
  });

  /* =========================================
     FILTRADO INICIAL
  ========================================= */

  filterCards();
});
