from sindex import get_version_number, get_first_species, get_species_code, get_species_name, calc_site, EAgeType, \
    EEstimate, calc_y2bh, calc_convert_site, calc_height, calc_site_class_to_site_index, EnumSiteClass, EnumCstIntFIZ

if __name__ == "__main__":
    # Example usage
    version = get_version_number()
    print("Version:", version)

    first_species = get_first_species()
    print("First Species Index:", first_species)

    if first_species != -1:
        species_code = get_species_code(first_species)
        print("Species Code:", species_code)

        species_name = get_species_name(first_species)
        print("Species Name:", species_name)

        # Example to calculate site index
        site_index = calc_site(1, 10.0, 50.0, EAgeType.TOTAL, EEstimate.DIRECT)
        print("Calculated Site Index:", site_index)

        # Example to calculate years to breast height
        y2bh = calc_y2bh(1, site_index)
        print("Years to Breast Height:", y2bh)

        # Example to convert site index to another species
        converted_site_index = calc_convert_site(first_species, site_index, 2)
        print("Converted Site Index:", converted_site_index)

        # Example to calculate height from site index and age
        height = calc_height(1, site_index, 50.0, 5.0, EAgeType.TOTAL)
        print("Calculated Height:", height)

        # Example to calculate site index from site class and FIZ
        site_index_from_class = calc_site_class_to_site_index(first_species, EnumSiteClass.MEDIUM, EnumCstIntFIZ.COAST)
        print("Site Index from Site Class:", site_index_from_class)