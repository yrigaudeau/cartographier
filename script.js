var tableauNbrTravauxVillage = % tableauNbrTravauxVillage %;
var tableauVillage = % tableauVillage %;
var tableauCatVillage = % tableauCatVillage %;

//console.log(tableauVillage);
//console.log(tableauCatVillage);

const maxScale = 10, minScale = 0.1;
var zoomMax = 0;

function reply_click(button) {
    var clList = button.classList;
    var add;
    var color = button.style.backgroundColor;
    if (clList.contains("active")) {
        clList.remove("active");
        add = -1;
    } else {
        clList.add("active");
        add = 1;
    }

    var categorie = button.id;
    for (let i = 0; i < tableauCatVillage[categorie].length; i++) {
        tableauVillage[tableauCatVillage[categorie][i]] += add;
        //console.log(tableauVillage[tableauCatVillage[categorie][i]]);
        update_circle(tableauCatVillage[categorie][i] + 'G', tableauVillage[tableauCatVillage[categorie][i]], color);
    }
}

function update_circle(id, nb, color = null) {
    var group = document.getElementById(id);
    var village = group.firstElementChild;
    var text = group.lastElementChild;
    var couleurs = [];

    if (nb > 0 || text.classList.contains("persistant")) {
        text.style.display = 'block';
    } else {
        text.style.display = 'none';
    }

    var textRemoved = group.removeChild(text);

    for (let i = group.children.length; i > 1; i--) {
        couleurs.push(group.lastElementChild.getAttribute('stroke'));
        var removed = group.removeChild(group.lastChild);
    }

    if (couleurs.length > nb) {
        couleurs.splice(couleurs.indexOf(color), 1);
    } else if (couleurs.length < nb) {
        couleurs.push(color);
    }
    //console.log(couleurs);

    for (let i = 0; i < nb; i++) {
        var circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");  //creation de l'élément dans le namespace svg
        var r = parseFloat(village.getAttribute('r'));
        var x = parseFloat(village.getAttribute('cx'));
        var y = parseFloat(village.getAttribute('cy'));
        circle.setAttribute('onclick', 'display(this.parentNode.id)')
        circle.setAttribute('r', r / 2);
        circle.setAttribute('cx', x);
        circle.setAttribute('cy', y);
        circle.setAttribute('fill', 'none');
        circle.setAttribute('stroke', couleurs[nb - 1 - i]);
        circle.setAttribute('stroke-width', r);
        circle.setAttribute('style', 'cursor: pointer')
        var proportion = r * Math.PI / nb;
        var tailleTotale = Math.PI * r;
        circle.setAttribute('stroke-dasharray', proportion + ' ' + tailleTotale);
        var angle_depart = i * 360 / nb - 90;
        circle.setAttribute('transform', 'rotate(' + angle_depart + ' ' + x + ' ' + y + ')');

        group.appendChild(circle);
    }

    group.appendChild(textRemoved);
}

function afficher_villages(button) {
    var clList = button.classList;
    if (clList.contains("active"))
        clList.remove("active");
    else
        clList.add("active");

    if (button.id == "PV") {
        var style = document.getElementById(button.id + 'G').style.display;
        if (style === "none")
            document.getElementById(button.id + 'G').style.display = "block";
        else
            document.getElementById(button.id + 'G').style.display = "none";
    }
    else if (button.id == "PT") {
        var cercles = document.querySelectorAll("circle:first-of-type");
        if (button.classList.contains("active")) {
            for (let i = 0; i < cercles.length; i++) {
                let id = cercles[i].parentElement.id.slice(0, -1);
                if (tableauNbrTravauxVillage[id] > 0) {
                    cercles[i].setAttribute("stroke", "white");
                    cercles[i].setAttribute("fill", "black");
                }
            }
        }
        else {
            for (let i = 0; i < cercles.length; i++) {
                let id = cercles[i].parentElement.id.slice(0, -1);
                if (tableauNbrTravauxVillage[id] > 0) {
                    cercles[i].setAttribute("stroke", "black");
                    cercles[i].setAttribute("fill", "white");
                }
            }
            let btnCategories = document.getElementsByClassName("categories");
            for (let i = 0; i < btnCategories.length; i++) {
                if (btnCategories[i].classList.contains("active")) {
                    btnCategories[i].click();
                }
            }
        }
    }
}

function display(id) {
    id = id.slice(0, -1);   //on enleve la derniere lettre

    var rect = document.getElementById(id + 'R');
    var group = rect.parentElement;
    if (rect.style.display === "none") {
        rect.style.display = "block";
        group.appendChild(rect);
    } else {
        rect.style.display = "none";
    }
}

//on simule la molette de la souris au centre de la carte pour zoomer avec les boutons
function btnzoom(direction) {
    var svgmap = document.getElementById('carte');
    var evt = new CustomEvent('btnzoom');
    evt.wheelDelta = direction * 10;

    var box = svgmap.getBoundingClientRect();
    evt.clientX = window.innerWidth + (box.left - box.right) / 2;
    evt.clientY = window.innerHeight + (box.top - box.bottom) / 2;

    document.getElementById('carte').dispatchEvent(evt);
}

function premierPlan(rect) {
    group = rect.parentElement;
    group.appendChild(rect);
}

function majEchelle(scale) {
    let echelle = document.getElementById("echelle");
    let valeurBase = echelle.getAttribute("valeurBase");
    echelle.innerHTML = "" + Math.round(valeurBase * (1 / scale)) + " km";
}

function majTailleNomVillages(scale) {
    var textes = document.getElementsByClassName("nomVillageCarte");
    for (let i = 0; i < textes.length; i++) {
        textes[i].style.fontSize = scale > 1 ? (1 / scale) * 20 + "px" : "20px";
    }
}

function majTailleCercleVillages(scale) {
    var cercles = document.querySelectorAll("circle:first-of-type");
    if (scale == maxScale && !zoomMax) {
        for (let i = 0; i < cercles.length; i++) {
            cercles[i].setAttribute("r", cercles[i].getAttribute("r") / 2);
            let id = cercles[i].parentElement.id.slice(0, -1);
            if (tableauVillage[id] > 0) {
                update_circle(id + 'G', tableauVillage[id]);
            }
        }
        zoomMax = 1;
    } else if (scale < maxScale && zoomMax) {
        for (let i = 0; i < cercles.length; i++) {
            cercles[i].setAttribute("r", cercles[i].getAttribute("r") * 2);
            let id = cercles[i].parentElement.id.slice(0, -1);
            if (tableauVillage[id] > 0) {
                update_circle(id + 'G', tableauVillage[id]);
            }
        }
        zoomMax = 0;
    }
}

//https://stackoverflow.com/questions/55453969/svg-object-how-to-zoom-and-drag-it-properly
var selected,
    scale = 1,
    svg = document.getElementById('carte');

function beginDrag(e) {
    e.stopPropagation();
    let target = e.target;

    if (target.classList.contains('draggable')) {
        selected = target;
    } else {
        selected = document.querySelector('#zoom');
    }

    selected.dataset.startMouseX = e.clientX;
    selected.dataset.startMouseY = e.clientY;
}

function drag(e) {
    if (!selected) return;
    e.stopPropagation();

    let startX = parseFloat(selected.dataset.startMouseX),
        startY = parseFloat(selected.dataset.startMouseY),
        dx = (e.clientX - startX),
        dy = (e.clientY - startY);

    if (selected.classList.contains('draggable')) {
        let selectedBox = selected.getBoundingClientRect(),
            boundaryBox = selected.parentElement.getBoundingClientRect();

        if (selectedBox.right + dx > boundaryBox.right) {
            dx = (boundaryBox.right - selectedBox.right);
        } else if (selectedBox.left + dx < boundaryBox.left) {
            dx = (boundaryBox.left - selectedBox.left);
        }

        if (selectedBox.bottom + dy > boundaryBox.bottom) {
            dy = (boundaryBox.bottom - selectedBox.bottom);
        }
        else if (selectedBox.top + dy < boundaryBox.top) {
            dy = (boundaryBox.top - selectedBox.top);
        }
    }

    let currentMatrix = selected.transform.baseVal.consolidate().matrix,
        newMatrix = currentMatrix.translate(dx / scale, dy / scale),
        transform = svg.createSVGTransformFromMatrix(newMatrix);

    selected.transform.baseVal.initialize(transform);
    selected.dataset.startMouseX = dx + startX;
    selected.dataset.startMouseY = dy + startY;
    //console.log(selected.dataset.startMouseX);
}

function endDrag(e) {
    e.stopPropagation();

    if (selected) {
        selected = undefined;
    }
}


function zoom(e) {
    e.stopPropagation();
    e.preventDefault();

    var delta;
    if (e.wheelDelta) {
        delta = e.wheelDelta;
    } else {
        delta = -e.detail;      //firefox
    }

    let container = document.querySelector('svg #zoom');
    let scaleStep = delta > 0 ? 1.25 : 0.8;

    if (scale * scaleStep > maxScale) {
        scaleStep = maxScale / scale;
    }

    if (scale * scaleStep < minScale) {
        scaleStep = minScale / scale;
    }

    scale *= scaleStep;

    let box = svg.getBoundingClientRect();
    let point = svg.createSVGPoint();
    point.x = e.clientX - box.left;
    point.y = e.clientY - box.top;

    let currentZoomMatrix = container.getCTM();

    point = point.matrixTransform(currentZoomMatrix.inverse());

    let matrix = svg.createSVGMatrix()
        .translate(point.x, point.y)
        .scale(scaleStep)
        .translate(-point.x, -point.y);


    let newZoomMatrix = currentZoomMatrix.multiply(matrix);
    container.transform.baseVal.initialize(svg.createSVGTransformFromMatrix(newZoomMatrix));
    //n'était pas présent dans la bibliothèque
    majEchelle(scale);
    majTailleNomVillages(scale);
    majTailleCercleVillages(scale);

    //console.log("scale", scale);
    //let t = newZoomMatrix;
    //console.log("zoomMatrix", t.a, t.b, t.c, t.d, t.e, t.f);
}

document.getElementById('carte').addEventListener('mousedown', beginDrag);
document.getElementById('carte').addEventListener('mousewheel', zoom);
document.getElementById('carte').addEventListener('DOMMouseScroll', zoom);     //firefox
document.getElementById('carte').addEventListener('btnzoom', zoom);            //boutons
svg.addEventListener('mousemove', drag);
window.addEventListener('mouseup', endDrag);
