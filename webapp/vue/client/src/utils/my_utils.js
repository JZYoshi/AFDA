function get_unit(var_name) {
  const spd_keywords = ["spd", "speed", "spind"];
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

export default get_unit;
