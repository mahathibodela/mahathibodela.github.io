const sentences = [
    "I'M AN AI ENTHUSIAST",
    "I LOVE TO CODE",
    "I'M INTERESTED IN PROBLEM SOLVING"
];
let currentSentence = 0;
let currentChar = 0;

function typeWriter() {
    const sentenceElement = document.getElementById('sentence');
    sentenceElement.style.display = 'block';
    sentenceElement.textContent = sentences[currentSentence].substring(0, currentChar + 1);
    currentChar++;

    if (currentChar === sentences[currentSentence].length) {
        setTimeout(() => {
            sentenceElement.style.display = 'none';
            currentChar = 0;
            currentSentence = (currentSentence + 1) % sentences.length;
            setTimeout(typeWriter, 100); // Pause before starting the next sentence
        }, 2000); // Pause after the sentence is fully displayed
    } else {
        setTimeout(typeWriter, 100); // Speed of typing
    }
}

document.addEventListener("DOMContentLoaded", () => {
    typeWriter();
});

let left = document.getElementById("second_left")
let right = document.getElementById("second_right")
let middle = document.getElementById("second_middle")

let leftHeight = left.style.height;
let rightHeight = left.style.height;

middle.style.maxHeight = Math.max(leftHeight, rightHeight)
console.log(middle.style.maxHeight)