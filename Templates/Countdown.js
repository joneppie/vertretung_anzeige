function countdown(time, factor = 1)
{
    time--;
    document.getElementById('countdown').style.width = time * factor + 'px';
    if(time > 0) {
        setTimeout('countdown(' + time +',' + factor + ')',1000);
    }
}
