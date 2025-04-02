// Add an event listener to detect when the window is resized
window.addEventListener("resize", event => {
    // When the window is resized, show an alert with the new width and height of the window
    alert(`${window.innerWidth}px x ${window.innerHeight}px`)
})
