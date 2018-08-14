function bodyOnLoad(){
    addImageInfo();
}

function addImageInfo(){
    var img = document.getElementById('image_0');
    var p_shape = document.getElementById('p_shape');
    p_shape.innerText = 'Shape: (height=' + img.height + ', ' + 'width=' + img.width + ')';
}