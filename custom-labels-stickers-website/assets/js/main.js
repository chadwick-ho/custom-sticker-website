const whatsappNumber = "8613285455519";
const whatsappMessages = {
  default: "Hello, I would like to request a quote for custom labels. My product, label size and quantity are...",
  vial: "Hello, I would like to request a quote for custom peptide vial labels. My vial size, label size and quantity are...",
  supplement: "Hello, I would like to request a quote for custom supplement labels. My bottle size, label size and quantity are...",
  hologram: "Hello, I would like to request a quote for custom 3D holographic labels. My label size, security effect and quantity are...",
  stickers: "Hello, I would like to request a quote for custom stickers. I can send my artwork, size and quantity.",
  beverage: "Hello, I would like to request a quote for custom beverage labels. My bottle type, label size and quantity are..."
};
const getWhatsappInquiryType = (link) => {
  const explicitType = link.dataset.whatsapp;
  if (explicitType && whatsappMessages[explicitType]) return explicitType;

  const sectionLabel = link.closest("section")?.getAttribute("aria-labelledby") || "";
  const context = `${window.location.pathname.toLowerCase()} ${sectionLabel.toLowerCase()}`;
  if (context.includes("hologram")) return "hologram";
  if (context.includes("supplement")) return "supplement";
  if (context.includes("peptide") || context.includes("vial")) return "vial";
  return "default";
};
const whatsappLinks = document.querySelectorAll("[data-whatsapp]");
whatsappLinks.forEach((link) => {
  const inquiryType = getWhatsappInquiryType(link);
  const message = whatsappMessages[inquiryType] || whatsappMessages.default;
  link.setAttribute("href", `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(message)}`);
  link.setAttribute("target", "_blank");
  link.setAttribute("rel", "noopener");
  link.setAttribute("aria-label", `${link.textContent.trim()} - opens WhatsApp in a new tab`);
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
