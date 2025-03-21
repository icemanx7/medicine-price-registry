from . import models

dosage_form = {
    "Liq" : "liquid",
    "Tab" : "tablet",
    "Cap" : "capsule",
    "Cps" : "capsule",
    "Oin" : "ointment",
    "Lit" : "lotion",
    "Lot" : "lotion",
    "Inj" : "injection",
    "Syr" : "syrup",
    "Dsp" : "effervescent tablet",
    "Eft" : "effervescent tablet",
    "Ear" : "drops",
    "Drp" : "drops",
    "Opd" : "drops",
    "Udv" : "vial",
    "Sus" : "suspension",
    "Susp" : "suspension",
    "Cal" : "calasthetic",
    "Sol" : "solution",
    "Sln" : "solution",
    "Neb" : "nebuliser",
    "Inh" : "inhaler",
    "Spo" : "inhaler",
    "Inf" : "infusion",
    "Chg" : "chewing Gum",
    "Vac" : "vacutainer",
    "Vag" : "vaginal gel",
    "Jel" : "gel",
    "Eyo" : "eye ointment",
    "Vat" : "vaginal cream",
    "Poi" : "injection",
    "Ped" : "powder",
    "Pow" : "powder",
    "Por" : "powder",
    "Sac" : "sachet",
    "Sup" : "suppository",
    "Cre" : "cream",
    "Ptd" : "patch",
    "Ped" : "penset",
    "Ect" : "tablet",
    "Nas" : "spray",
}

def as_currency(x):
    try:
        x = float(x)
        return "R %.2f" % x
    except (ValueError, TypeError):
        return "-"

def int_or_float(x):
    try:
        x = float(x)
        if int(x) == float(x):
            return int(x)
        return x
    except (ValueError, TypeError):
        return "-"
    
def serialize_ingredient(ingredient, strength):
    return {
        "name" : ingredient.name,
        "unit" : ingredient.unit,
        "strength" : int_or_float(strength),
    }

def serialize_product(product):
    return {
        "id" : product.id,
        "nappi_code" : product.nappi_code,
        "regno" : product.regno.upper(),
        "schedule" : product.schedule,
        "name" : product.name,
        "dosage_form" : dosage_form.get(product.dosage_form, product.dosage_form),
        "pack_size" : product.pack_size,
        "num_packs" : product.num_packs,
        "sep" : as_currency(product.max_fee),
        "cost_per_unit" : as_currency(product.cost_per_unit),
        "dispensing_fee" : as_currency(product.dispensing_fee),
        "is_generic" : product.is_generic,
        "ingredients" : [
            serialize_ingredient(pi.ingredient, pi.strength)
            for pi in product.product_ingredients.all()
        ],
        "number_of_generics" : len(product.related_products),
        "copayments": product.copayments
    }

def serialize_product_apiv3(product):
    details = serialize_product(product)
    details["sep"] = as_currency(product.sep)
    details["min_price"] = as_currency(product.sep)
    details["max_price"] = as_currency(product.sep + product.dispensing_fee)
    details["min_cost_per_unit"] = as_currency(product.min_cost_per_unit)
    details["max_cost_per_unit"] = as_currency(product.max_cost_per_unit)

    return details

def serialize_products(products):
    return [serialize_product(p) for p in products]

def serialize_product_lite(product):
    name = product.name
    if product.ingredients.all().count() == 1:
        ingredient = product.ingredients.all()[0]
        pi = models.ProductIngredient.objects.get(product=product, ingredient=ingredient)
        form = dosage_form.get(product.dosage_form, product.dosage_form)
        name = "%s (%s%s %s)" % (name, int_or_float(pi.strength), ingredient.unit, form)

    return {
        "id" : product.id,
        "nappi_code" : product.nappi_code,
        "name" : name,
        "dosage_form" : dosage_form.get(product.dosage_form, product.dosage_form),
        "sep" : as_currency(product.max_fee),
        "number_of_generics" : len(product.related_products),
    }

def serialize_products_lite(products):
    return [serialize_product_lite(p) for p in products]
