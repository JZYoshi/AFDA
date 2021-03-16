function get_unit(var_name) {
  const spd_keywords = ["spd", "speed"];
  const temp_keywords = ["temp", "dewpoint"];
  const altitude_keywords = ["altitude"];
  const duration_keywords = ["duration"];
  const ingredients = var_name.trim().split("_");
  if (ingredients.filter(i => spd_keywords.includes(i)).length != 0) {
    return "m/s";
  } else if (ingredients.filter(i => temp_keywords.includes(i)).length != 0) {
    return "Celsius";
  } else if (
    ingredients.filter(i => altitude_keywords.includes(i)).length != 0
  ) {
    return "m";
  } else if (
    ingredients.filter(i => duration_keywords.includes(i)).length != 0
  ) {
    return "s";
  } else {
    return "";
  }
}

function getRandomRgb() {
  var num = Math.round(0xffffff * Math.random());
  var r = num >> 16;
  var g = (num >> 8) & 255;
  var b = num & 255;
  return "rgb(" + r + ", " + g + ", " + b + ")";
}

// group number starts from 1
function generateGroupColors(group_list) {
  let group_color_list = [];
  return group_list.map(group => {
    if (group > group_color_list.length) {
      for (let i = 0; i < group - group_color_list.length; i++) {
        let color = getRandomRgb();
        group_color_list.push(color);
      }
      return group_color_list[group_color_list.length - 1];
    } else {
      return group_color_list[group - 1];
    }
  });
}

export { get_unit, getRandomRgb, generateGroupColors };
