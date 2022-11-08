// document.querySelectorAll("pre").length;

// document.querySelectorAll("pre>code");

// document.querySelectorAll("pre>code.language-bash")[2].innerHTML;

// var h = document.querySelectorAll("pre>code");
// h.forEach((i) => console.log(i.innerHTML));

// document.querySelectorAll("pre>code").forEach((i) => console.log(i.innerHTML));

// Array.prototype.filter();

// var turkey = Array.prototype.filter.call(sandwiches, function (sandwich) {
//   return sandwich.matches(".turkey");
// });

// Array.prototype.filter.call(h, function (i) {
//   return i.matches(".language-bash");
// });

// Array.prototype.filter.call(h, function (i) {
//   return i.innerHTML.includes("Docker");
// });

https://jshint.com/docs/options

// First Table
let el = document.querySelector("[href='#enforcing-options']");
document.querySelector("h3>a[href='#enforcing-options']").parentElement;
let t = document.querySelector("table"); // first table, should be the enforcing one
let thing = Array.from(t.querySelectorAll("tr>td[id]")); // the ids
thing.map(i => {return i.id + ": true"}).join(", ");
