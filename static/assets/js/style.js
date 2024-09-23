$('.sec-modal').click(function(){
    target = $(this).data('target');
    $('.sec-modal').removeClass('text-primary');
    $('.sec-modal').removeClass('underline');
    $(this).addClass('underline');
    $(this).addClass('text-primary');
    $('.sec-target').addClass('d-none');
    $('#'+target).removeClass('d-none');
})