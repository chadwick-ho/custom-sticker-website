const whatsappUrl = "https://wa.me/8613285455519?text=Hi%20RP%20Labels%2C%20I%20saw%20your%20custom%20labels%20on%20rplabels.com.%20I%27d%20like%20a%20quote%20and%20free%20design%20help%20for%20my%20project.%20Can%20we%20chat%3F";
const whatsappLinks = document.querySelectorAll("[data-whatsapp]");
whatsappLinks.forEach((link) => {
  link.setAttribute("href", whatsappUrl);
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
