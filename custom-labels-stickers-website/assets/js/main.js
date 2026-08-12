const whatsappUrl = "https://api.whatsapp.com/message/AWJL6N3AAGIZA1?autoload=1&app_absent=0";
const whatsappMessages = {
  default: "Hello, I would like to get a quote for custom labels and stickers.",
  vial: "Hello, I would like to get a quote for custom peptide vial labels. My label size and quantity are...",
  stickers: "Hello, I would like to customize cartoon stickers. I can send my design and quantity.",
  beverage: "Hello, I would like to get a quote for custom beverage labels. My bottle type and quantity are..."
};
const whatsappLinks = document.querySelectorAll("[data-whatsapp]");
whatsappLinks.forEach((link) => {
  link.setAttribute("href", whatsappUrl);
  link.setAttribute("target", "_blank");
  link.setAttribute("rel", "noopener");
});

const toggle = document.querySelector(".mobile-toggle");
const nav = document.querySelector(".main-nav");
if (toggle && nav) {
  toggle.addEventListener("click", () => {
    const open = nav.classList.toggle("is-open");
    toggle.setAttribute("aria-expanded", String(open));
  });
}

document.querySelectorAll(".faq-button").forEach((button) => {
  button.addEventListener("click", () => {
    const item = button.closest(".faq-item");
    item.classList.toggle("is-open");
    button.setAttribute("aria-expanded", String(item.classList.contains("is-open")));
  });
});

document.querySelectorAll("form[data-inquiry-form]").forEach((form) => {
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const message = form.querySelector(".success-message");
    if (message) message.classList.add("show");
    form.reset();
  });
});

document.querySelectorAll("[data-product-gallery]").forEach((gallery) => {
  const main = gallery.querySelector("[data-product-main]");
  const thumbs = gallery.querySelectorAll("[data-product-thumb]");
  thumbs.forEach((thumb) => {
    thumb.addEventListener("click", () => {
      if (!main) return;
      const image = thumb.querySelector("img");
      if (!image) return;
      main.src = image.src;
      main.alt = image.alt;
      thumbs.forEach((item) => item.classList.remove("is-active"));
      thumb.classList.add("is-active");
    });
  });
});

document.querySelectorAll("img").forEach((img) => {
  img.addEventListener("error", () => {
    img.style.display = "none";
    img.parentElement.classList.add("image-fallback");
  });
});
