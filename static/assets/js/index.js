if( $('.page_hero-talents_items').length ){
    var myVar = setInterval(() => {
      let parent = document.querySelector('.page_hero-talents_items');
      if(parent){
          let children = parent.children;
          let changeItem = children[0];
          parent.removeChild(changeItem);
          parent.appendChild(changeItem);
      }
    }, 4000);
}
if( $('.page_hero-talents_items2').length ){
    var myVar = setInterval(() => {
      let parent = document.querySelector('.page_hero-talents_items2');
      if(parent){
          let children = parent.children;
          let changeItem = children[0];
          parent.removeChild(changeItem);
          parent.appendChild(changeItem);
      }
    }, 4000);
}
