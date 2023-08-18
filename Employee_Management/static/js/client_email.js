const dropdowns = document.querySelectorAll('.dropdown');
  
    dropdowns.forEach(dropdown => {
      const content = dropdown.nextElementSibling;
      dropdown.addEventListener('click', () => {
        dropdown.classList.toggle('active');

        if(dropdown.classList.contains('active')){
          content.style.transform = 'translateY(120px)';
        }else{
          content.style.transform='none';
        }
      });
    });
    const productsDropdown = document.getElementById('productsDropdown');
    const servicesDropdown = document.getElementById('servicesDropdown');
    const dynamicContent = document.getElementById('dynamicContent');
    const defaultContent = document.getElementById('defaultContent').innerHTML;
    const productsContent = document.getElementById('productsContent').innerHTML;
    const servicesContent = document.getElementById('servicesContent').innerHTML;
  
    let showProductsContent = false;
  
    productsDropdown.addEventListener('click', () => {
      if (showProductsContent) {
        dynamicContent.innerHTML = defaultContent;
        showProductsContent = false;
      } else {
        dynamicContent.innerHTML = productsContent;
        showProductsContent = true;
      }
    });

    let showServicesContent = false;

    servicesDropdown.addEventListener('click',()=>{
      if(showServicesContent){
        dynamicContent.innerHTML = defaultContent;
        showServicesContent = false;
      }else{
        dynamicContent.innerHTML = servicesContent;
        showServicesContent = true;
      }
    });