"""Material Schema"""
from pydantic import Field, validator, root_validator, constr, confloat
from typing import Union, List
from enum import Enum

from ._base import IDdEnergyBaseModel
from ..altnumber import Autocalculate


class Roughness(str, Enum):
    """Relative roughness of a particular material layer."""
    very_rough = 'VeryRough'
    rough = 'Rough'
    medium_rough = 'MediumRough'
    medium_smooth = 'MediumSmooth'
    smooth = 'Smooth'
    very_smooth = 'VerySmooth'


class MoistureDiffusionModel(str, Enum):
    """Acceptable values for the moisture diffusion model for vegetation."""
    simple = 'Simple'
    advanced = 'Advanced'


class EnergyMaterialNoMass(IDdEnergyBaseModel):
    """No mass opaque material representing a layer within an opaque construction.

    Used when only the thermal resistance (R value) of the material is known.
    """

    type: constr(regex='^EnergyMaterialNoMass$') = 'EnergyMaterialNoMass'

    r_value: float = Field(
        ...,
        ge=0.001,
        description='The thermal resistance (R-value) of the material layer [m2-K/W].'
    )

    roughness: Roughness = Roughness.medium_rough

    thermal_absorptance: float = Field(
        0.9,
        gt=0,
        le=0.99999,
        description='Fraction of incident long wavelength radiation that is absorbed by'
        ' the material. Default: 0.9.'
    )

    solar_absorptance: float = Field(
        0.7,
        ge=0,
        le=1,
        description='Fraction of incident solar radiation absorbed by the material.'
        ' Default: 0.7.'
    )

    visible_absorptance: float = Field(
        0.7,
        ge=0,
        le=1,
        description='Fraction of incident visible wavelength radiation absorbed by the'
        ' material. Default: 0.7.'
    )


class EnergyMaterial(IDdEnergyBaseModel):
    """Opaque material representing a layer within an opaque construction."""

    type: constr(regex='^EnergyMaterial$') = 'EnergyMaterial'

    roughness: Roughness = Roughness.medium_rough

    thickness: float = Field(
        ...,
        gt=0,
        le=3,
        description='Thickness of the material layer in meters.'
    )

    conductivity: float = Field(
        ...,
        gt=0,
        description='Thermal conductivity of the material layer in W/m-K.',
    )

    density: float = Field(
        ...,
        gt=0,
        description='Density of the material layer in kg/m3.'
    )

    specific_heat: float = Field(
        ...,
        ge=100,
        description='Specific heat of the material layer in J/kg-K.'
    )

    thermal_absorptance: float = Field(
        0.9,
        gt=0,
        le=0.99999,
        description='Fraction of incident long wavelength radiation that is absorbed by'
        ' the material. Default: 0.9.'
    )

    solar_absorptance: float = Field(
        0.7,
        ge=0,
        le=1,
        description='Fraction of incident solar radiation absorbed by the material.'
        ' Default: 0.7.'
    )

    visible_absorptance: float = Field(
        0.7,
        ge=0,
        le=1,
        description='Fraction of incident visible wavelength radiation absorbed by the'
        ' material. Default: 0.7.'
    )


class EnergyMaterialVegetation(IDdEnergyBaseModel):
    """Material representing vegetation on the exterior of an opaque construction."""

    type: constr(regex='^EnergyMaterialVegetation$') = 'EnergyMaterialVegetation'

    roughness: Roughness = Roughness.medium_rough

    thickness: float = Field(
        0.1,
        gt=0,
        le=3,
        description='Thickness of the soil layer in meters.'
    )

    conductivity: float = Field(
        0.35,
        gt=0,
        description='Thermal conductivity of the dry soil in W/m-K.',
    )

    density: float = Field(
        1100,
        gt=0,
        description='Density of the dry soil in kg/m3.'
    )

    specific_heat: float = Field(
        1200,
        ge=100,
        description='Specific heat of the dry soil in J/kg-K.'
    )

    soil_thermal_absorptance: float = Field(
        0.9,
        gt=0,
        le=0.99999,
        description='Fraction of incident long wavelength radiation that is absorbed by'
        ' the soil. Default: 0.9.'
    )

    soil_solar_absorptance: float = Field(
        0.7,
        ge=0,
        le=1,
        description='Fraction of incident solar radiation absorbed by the soil.'
        ' Default: 0.7.'
    )

    soil_visible_absorptance: float = Field(
        0.7,
        ge=0,
        le=1,
        description='Fraction of incident visible wavelength radiation absorbed by the'
        ' material. Default: 0.7.'
    )

    plant_height: float = Field(
        0.2,
        ge=0.005,
        le=1.0,
        description='The height of plants in the vegetation in meters.'
    )

    leaf_area_index: float = Field(
        1.0,
        ge=0.001,
        le=5.0,
        description='The projected leaf area per unit area of soil surface '
        '(aka. Leaf Area Index or LAI). Note that the fraction of vegetation '
        'cover is calculated directly from LAI using an empirical relation.'
    )

    leaf_reflectivity: float = Field(
        0.22,
        ge=0.005,
        le=0.5,
        description='The fraction of incident solar radiation that is reflected '
        'by the leaf surfaces. Solar radiation includes the visible spectrum as '
        'well as infrared and ultraviolet wavelengths. Typical values are 0.18 to 0.25.'
    )

    leaf_emissivity: float = Field(
        0.95,
        ge=0.8,
        le=1.0,
        description='The ratio of thermal radiation emitted from leaf surfaces to '
        'that emitted by an ideal black body at the same temperature.'
    )

    min_stomatal_resist: float = Field(
        180,
        ge=50,
        le=300,
        description='The resistance of the plants to moisture transport [s/m]. '
        'Plants with low values of stomatal resistance will result in higher '
        'evapotranspiration rates than plants with high resistance.'
    )

    sat_vol_moist_cont: float = Field(
        0.3,
        ge=0.1,
        le=0.5,
        description='The saturation moisture content of the soil by volume.'
    )

    residual_vol_moist_cont: float = Field(
        0.01,
        ge=0.01,
        le=0.1,
        description='The residual moisture content of the soil by volume.'
    )

    init_vol_moist_cont: float = Field(
        0.01,
        ge=0.05,
        le=0.5,
        description='The initial moisture content of the soil by volume.'
    )

    moist_diff_model: MoistureDiffusionModel = MoistureDiffusionModel.simple


class EnergyWindowMaterialSimpleGlazSys(IDdEnergyBaseModel):
    """Describe an entire glazing system rather than individual layers.

    Used when only very limited information is available on the glazing layers or when
    specific performance levels are being targeted.
    """

    type: constr(regex='^EnergyWindowMaterialSimpleGlazSys$') = \
        'EnergyWindowMaterialSimpleGlazSys'

    u_factor: float = Field(
        ...,
        gt=0,
        le=12,
        description='The overall heat transfer coefficient for window system in W/m2-K. '
        'Note that constructions with U-values above 5.8 should not be assigned to '
        'skylights as this implies the resistance of the window is negative when '
        'air films are subtracted.'
    )

    shgc: float = Field(
        ...,
        gt=0,
        lt=1,
        description='Unit-less quantity for the Solar Heat Gain Coefficient (solar '
        'transmittance + conduction) at normal incidence and vertical orientation.'
    )

    vt: float = Field(
        0.54,
        gt=0,
        lt=1,
        description='The fraction of visible light falling on the window that makes it'
        ' through the glass at normal incidence.'
    )


class EnergyWindowMaterialGlazing(IDdEnergyBaseModel):
    """Describe a single glass pane corresponding to a layer in a window construction."""

    type: constr(regex='^EnergyWindowMaterialGlazing$') = 'EnergyWindowMaterialGlazing'

    thickness: float = Field(
        0.003,
        gt=0,
        description='The surface-to-surface thickness of the glass in meters. Default: '
        ' 0.003.'
    )

    solar_transmittance: float = Field(
        0.85,
        ge=0,
        le=1,
        description='Transmittance of solar radiation through the glass at normal'
        ' incidence. Default: 0.85 for clear glass.'
    )

    solar_reflectance: float = Field(
        0.075,
        ge=0,
        le=1,
        description='Reflectance of solar radiation off of the front side of the glass'
        ' at normal incidence, averaged over the solar spectrum. Default: 0.075'
        ' for clear glass.'
    )

    solar_reflectance_back: Union[Autocalculate, float] = Field(
        default=Autocalculate(),
        description='Reflectance of solar radiation off of the back side of the glass at'
        ' normal incidence, averaged over the solar spectrum.'
    )

    visible_transmittance: float = Field(
        0.9,
        ge=0,
        le=1,
        description='Transmittance of visible light through the glass at '
        'normal incidence. Default: 0.9 for clear glass.'
    )

    visible_reflectance: float = Field(
        0.075,
        ge=0,
        le=1,
        description='Reflectance of visible light off of the front side of the glass at'
        ' normal incidence. Default: 0.075 for clear glass.'
    )

    visible_reflectance_back: Union[Autocalculate, float] = Field(
        default=Autocalculate(),
        ge=0,
        le=1,
        description='Reflectance of visible light off of the back side of the glass at'
        ' normal incidence averaged over the solar spectrum and weighted by the response'
        ' of the human eye.'
    )

    infrared_transmittance: float = Field(
        0,
        ge=0,
        le=1,
        description='Long-wave transmittance at normal incidence.'
    )

    emissivity: float = Field(
        0.84,
        ge=0,
        le=1,
        description='Infrared hemispherical emissivity of the front (outward facing)'
        ' side of the glass.  Default: 0.84, which is typical for clear glass'
        ' without a low-e coating.'
    )

    emissivity_back: float = Field(
        0.84,
        ge=0,
        le=1,
        description='Infrared hemispherical emissivity of the back (inward facing) side'
        ' of the glass.  Default: 0.84, which is typical for clear glass without'
        ' a low-e coating.'
    )

    conductivity: float = Field(
        0.9,
        gt=0,
        description='Thermal conductivity of the glass in W/(m-K). Default: 0.9,'
        ' which is  typical for clear glass without a low-e coating.'
    )

    dirt_correction: float = Field(
        1,
        description='Factor that corrects for the presence of dirt on the glass. A'
        ' default value of 1 indicates the glass is clean.'
    )

    solar_diffusing: bool = Field(
        False,
        description='If False (default), the beam solar radiation incident on the '
        'glass is transmitted as beam radiation with no diffuse component.'
        'If True, the beam  solar radiation incident on the glass is transmitted as '
        'hemispherical diffuse radiation with no beam component.'
    )


class EnergyWindowFrame(IDdEnergyBaseModel):
    """Opaque material representing a layer within an opaque construction."""

    type: constr(regex='^EnergyWindowFrame$') = 'EnergyWindowFrame'

    width: float = Field(
        ...,
        gt=0,
        le=1,
        description='Number for the width of frame in plane of window [m]. '
        'The frame width is assumed to be the same on all sides of window..'
    )

    conductance: float = Field(
        ...,
        gt=0,
        description='Number for the thermal conductance of the frame material '
        'measured from inside to outside of the frame surface (no air films) '
        'and taking 2D conduction effects into account [W/m2-K].',
    )

    edge_to_center_ratio: float = Field(
        1,
        gt=0,
        le=4,
        description='Number between 0 and 4 for the ratio of the glass '
        'conductance near the frame (excluding air films) divided by the glass '
        'conductance at the center of the glazing (excluding air films). '
        'This is used only for multi-pane glazing constructions. This ratio should '
        'usually be greater than 1.0 since the spacer material that separates '
        'the glass panes is usually more conductive than the gap between panes. '
        'A value of 1 effectively indicates no spacer. Values should usually be '
        'obtained from the LBNL WINDOW program so that the unique characteristics '
        'of the window construction can be accounted for.'
    )

    outside_projection: float = Field(
        0,
        ge=0,
        le=0.5,
        description='Number for the distance that the frame projects outward from '
        'the outside face of the glazing [m]. This is used to calculate shadowing '
        'of frame onto glass, solar absorbed by the frame, IR emitted and '
        'absorbed by the frame, and convection from frame.'
    )

    inside_projection: float = Field(
        0,
        ge=0,
        le=0.5,
        description='Number for the distance that the frame projects inward from '
        'the inside face of the glazing [m]. This is used to calculate solar '
        'absorbed by the frame, IR emitted and absorbed by the frame, and '
        'convection from frame.'
    )

    thermal_absorptance: float = Field(
        0.9,
        gt=0,
        le=0.99999,
        description='Fraction of incident long wavelength radiation that is absorbed by'
        ' the frame material.'
    )

    solar_absorptance: float = Field(
        0.7,
        ge=0,
        le=1,
        description='Fraction of incident solar radiation absorbed by the '
        'frame material.'
    )

    visible_absorptance: float = Field(
        0.7,
        ge=0,
        le=1,
        description='Fraction of incident visible wavelength radiation absorbed by the'
        ' frame material.'
    )


class GasType (str, Enum):
    air = 'Air'
    argon = 'Argon'
    krypton = 'Krypton'
    xenon = 'Xenon'


class EnergyWindowMaterialGas(IDdEnergyBaseModel):
    """Create single layer of gas in a window construction.

    Can be combined with EnergyWindowMaterialGlazing to make multi-pane windows.
    """

    type: constr(regex='^EnergyWindowMaterialGas$') = 'EnergyWindowMaterialGas'

    thickness: float = Field(
        0.0125,
        gt=0,
        description='Thickness of the gas layer in meters. Default: 0.0125.'
    )

    gas_type: GasType = GasType.air


class EnergyWindowMaterialGasMixture(IDdEnergyBaseModel):
    """Create a mixture of two to four different gases to fill the panes of multiple
    pane windows."""

    type: constr(regex='^EnergyWindowMaterialGasMixture$') = \
        'EnergyWindowMaterialGasMixture'

    thickness: float = Field(
        0.0125,
        gt=0,
        description='The thickness of the gas mixture layer in meters.'
    )

    gas_types: List[GasType] = Field(
        ...,
        min_items=2,
        max_items=4,
        description='List of gases in the gas mixture.'
    )

    gas_fractions: List[confloat(gt=0, lt=1)] = Field(
        ...,
        min_items=2,
        max_items=4,
        description='A list of fractional numbers describing the volumetric fractions '
        'of gas types in the mixture. This list must align with the gas_types '
        'list and must sum to 1.'
    )

    @validator('gas_fractions')
    def check_sum(cls, v):
        """Check that fractions sum to 1."""
        assert abs(1 - sum(v)) < 0.001, 'gas_fractions must sum to 1.'
        return v

    @root_validator
    def check_types_fractions_match(cls, values):
        "Ensure the gas types and fractions match."
        gas_types = values.get('gas_types')
        gas_fractions = values.get('gas_fractions')
        assert len(gas_types) == len(gas_fractions), 'Length of gas_types must match ' \
            'length of gas_fractions. {} != {}'.format(
                len(gas_types), len(gas_fractions))
        return values


class EnergyWindowMaterialGasCustom(IDdEnergyBaseModel):
    """Create single layer of custom gas."""

    type: constr(regex='^EnergyWindowMaterialGasCustom$') = \
        'EnergyWindowMaterialGasCustom'

    thickness: float = Field(
        0.0125,
        gt=0,
        description='Thickness of the gas layer in meters. Default: 0.0125.'
    )

    conductivity_coeff_a: float = Field(
        ...,
        description='The A coefficient for gas conductivity in W/(m-K).'
    )

    conductivity_coeff_b: float = Field(
        0,
        description='The B coefficient for gas conductivity in W/(m-K2).'
    )

    conductivity_coeff_c: float = Field(
        0,
        description='The C coefficient for gas conductivity in W/(m-K3).'
    )

    viscosity_coeff_a: float = Field(
        ...,
        gt=0,
        description='The A coefficient for gas viscosity in kg/(m-s).'
    )

    viscosity_coeff_b: float = Field(
        0,
        description='The B coefficient for gas viscosity in kg/(m-s-K).'
    )

    viscosity_coeff_c: float = Field(
        0,
        description='The C coefficient for gas viscosity in kg/(m-s-K2).'
    )

    specific_heat_coeff_a: float = Field(
        ...,
        gt=0,
        description='The A coefficient for gas specific heat in J/(kg-K).'
    )

    specific_heat_coeff_b: float = Field(
        0,
        description='The B coefficient for gas specific heat in J/(kg-K2).'
    )

    specific_heat_coeff_c: float = Field(
        0,
        description='The C coefficient for gas specific heat in J/(kg-K3).'
    )

    specific_heat_ratio: float = Field(
        ...,
        gt=1,
        description='The specific heat ratio for gas.'
    )

    molecular_weight: float = Field(
        ...,
        ge=20,
        le=200,
        description='The molecular weight for gas in g/mol.'
    )


class EnergyWindowMaterialShade(IDdEnergyBaseModel):
    """This object specifies the properties of window shade materials."""

    type: constr(regex='^EnergyWindowMaterialShade$') = 'EnergyWindowMaterialShade'

    solar_transmittance: float = Field(
        0.4,
        ge=0,
        lt=1,
        description='The transmittance averaged over the solar spectrum. It is assumed'
        ' independent of incidence angle. Default: 0.4.'
    )

    solar_reflectance: float = Field(
        0.5,
        ge=0,
        lt=1,
        description='The reflectance averaged over the solar spectrum. It us assumed'
        ' same on both sides of shade and independent of incidence angle. Default'
        ' value is 0.5'
    )

    visible_transmittance: float = Field(
        0.4,
        ge=0,
        lt=1,
        description='The transmittance averaged over the solar spectrum and weighted by'
        ' the response of the human eye. It is assumed independent of incidence angle.'
        ' Default: 0.4.'
    )

    visible_reflectance: float = Field(
        0.4,
        ge=0,
        lt=1,
        description='The transmittance averaged over the solar spectrum and weighted by'
        ' the response of the human eye. It is assumed independent of incidence angle.'
        ' Default: 0.4'
    )

    emissivity: float = Field(
        0.9,
        gt=0,
        lt=1,
        description='The effective long-wave infrared hemispherical emissivity. It is'
        ' assumed same on both sides of shade. Default: 0.9.'
    )

    infrared_transmittance: float = Field(
        0,
        ge=0,
        lt=1,
        description='The effective long-wave transmittance. It is assumed independent'
        ' of incidence angle. Default: 0.'
    )

    thickness: float = Field(
        0.005,
        gt=0,
        description='The thickness of the shade material in meters. Default:'
        ' 0.005.'
    )

    conductivity: float = Field(
        0.1,
        gt=0,
        description='The conductivity of the shade material in W/(m-K). Default value'
        ' is 0.1.'
    )

    distance_to_glass: float = Field(
        0.05,
        ge=0.001,
        le=1,
        description='The distance from shade to adjacent glass in meters. Default value'
        ' is 0.05'
    )

    top_opening_multiplier: float = Field(
        0.5,
        ge=0,
        le=1,
        description='The effective area for air flow at the top of the shade, divided by'
        ' the horizontal area between glass and shade. Default: 0.5.'
    )

    bottom_opening_multiplier: float = Field(
        0.5,
        ge=0,
        le=1,
        description='The effective area for air flow at the bottom of the shade, divided'
        ' by the horizontal area between glass and shade. Default: 0.5.'
    )

    left_opening_multiplier: float = Field(
        0.5,
        ge=0,
        le=1,
        description='The effective area for air flow at the left side of the shade,'
        ' divided by the vertical area between glass and shade. Default: 0.5.'
    )

    right_opening_multiplier: float = Field(
        0.5,
        ge=0,
        le=1,
        description='The effective area for air flow at the right side of the shade,'
        ' divided by the vertical area between glass and shade. Default: 0.5.'
    )

    airflow_permeability: float = Field(
        0,
        ge=0,
        le=0.8,
        description='The fraction of the shade surface that is open to air flow.'
        ' If air cannot pass through the shade material, airflow_permeability = 0.'
        ' Default: 0.'
    )


class SlatOrientation (str, Enum):
    horizontal = 'Horizontal'
    vertical = 'Vertical'


class EnergyWindowMaterialBlind(IDdEnergyBaseModel):
    """Window blind material consisting of flat, equally-spaced slats."""

    type: constr(regex='^EnergyWindowMaterialBlind$') = 'EnergyWindowMaterialBlind'

    slat_orientation: SlatOrientation = SlatOrientation.horizontal

    slat_width: float = Field(
        0.025,
        gt=0,
        le=1,
        description='The width of slat measured from edge to edge in meters.'
    )

    slat_separation: float = Field(
        0.01875,
        gt=0,
        le=1,
        description='The distance between the front of a slat and the back of the'
        ' adjacent slat in meters.'
    )

    slat_thickness: float = Field(
        0.001,
        gt=0,
        le=0.1,
        description='The distance between the faces of a slat in meters. The default'
        ' value is 0.001.'
    )

    slat_angle: float = Field(
        45,
        ge=0,
        le=180,
        description='The angle (degrees) between the glazing outward normal and the slat'
        ' outward normal where the outward normal points away from the front face of the'
        ' slat (degrees). The default value is 45.'
    )

    slat_conductivity: float = Field(
        221,
        gt=0,
        description='The thermal conductivity of the slat in W/(m-K). Default:'
        ' 221.'
    )

    beam_solar_transmittance: float = Field(
        0,
        ge=0,
        lt=1,
        description='The beam solar transmittance of the slat, assumed to be independent'
        ' of angle of incidence on the slat. Any transmitted beam radiation is assumed'
        ' to be 100% diffuse (i.e., slats are translucent). The default value is 0.'
    )

    beam_solar_reflectance: float = Field(
        0.5,
        ge=0,
        lt=1,
        description='The beam solar reflectance of the front side of the slat, it is'
        ' assumed to be independent of the angle of incidence. Default: 0.5.'
    )

    beam_solar_reflectance_back: float = Field(
        0.5,
        ge=0,
        lt=1,
        description='The beam solar reflectance of the back side of the slat, it is'
        ' assumed to be independent of the angle of incidence. Default: 0.5.'
    )

    diffuse_solar_transmittance: float = Field(
        0,
        ge=0,
        lt=1,
        description='The slat transmittance for hemispherically diffuse solar radiation.'
        ' Default: 0.'
    )

    diffuse_solar_reflectance: float = Field(
        0.5,
        ge=0,
        lt=1,
        description='The front-side slat reflectance for hemispherically diffuse solar'
        ' radiation. Default: 0.5.'
    )

    diffuse_solar_reflectance_back: float = Field(
        0.5,
        ge=0,
        lt=1,
        description='The back-side slat reflectance for hemispherically diffuse solar'
        ' radiation. Default: 0.5.'
    )

    beam_visible_transmittance: float = Field(
        0,
        ge=0,
        lt=1,
        description='The beam visible transmittance of the slat, it is assumed to be'
        ' independent of the angle of incidence. Default: 0.'
    )

    beam_visible_reflectance: float = Field(
        0.5,
        ge=0,
        lt=1,
        description='The beam visible reflectance on the front side of the slat, it is'
        ' assumed to be independent of the angle of incidence. Default: 0.5.'
    )

    beam_visible_reflectance_back: float = Field(
        0.5,
        ge=0,
        lt=1,
        description='The beam visible reflectance on the back side of the slat, it is'
        ' assumed to be independent of the angle of incidence. Default: 0.5.'
    )

    diffuse_visible_transmittance: float = Field(
        0,
        ge=0,
        lt=1,
        description='The slat transmittance for hemispherically diffuse visible'
        ' radiation. This value should equal “Slat Beam Visible Transmittance.”'
    )

    diffuse_visible_reflectance: float = Field(
        0.5,
        ge=0,
        lt=1,
        description='The front-side slat reflectance for hemispherically diffuse visible'
        ' radiation. This value should equal “Front Side Slat Beam Visible Reflectance.”'
        ' Default: 0.5.'
    )

    diffuse_visible_reflectance_back: float = Field(
        0.5,
        ge=0,
        lt=1,
        description='The back-side slat reflectance for hemispherically diffuse visible'
        ' radiation. This value should equal “Back Side Slat Beam Visible Reflectance.'
        ' Default: 0.5.”'
    )

    infrared_transmittance: float = Field(
        0,
        ge=0,
        lt=1,
        description='The slat infrared hemispherical transmittance. It is zero for '
        'solid metallic, wooden or glass slats, but may be non-zero in some cases '
        'such as for thin plastic slats. The default value is 0.'
    )

    emissivity: float = Field(
        0.9,
        ge=0,
        lt=1,
        description='Front side hemispherical emissivity of the slat. Default is 0.9 for'
        ' most materials. The default value is 0.9.'
    )

    emissivity_back: float = Field(
        0.9,
        ge=0,
        lt=1,
        description='Back side hemispherical emissivity of the slat. Default is 0.9 for'
        ' most materials. The default value is 0.9.'
    )

    distance_to_glass: float = Field(
        0.05,
        ge=0.01,
        le=1,
        description='The distance from the mid-plane of the blind to the adjacent glass'
        ' in meters. The default value is 0.05.'
    )

    top_opening_multiplier: float = Field(
        0.5,
        ge=0,
        le=1,
        description='The effective area for air flow at the top of the shade, divided by'
        ' the horizontal area between glass and shade.'
    )

    bottom_opening_multiplier: float = Field(
        0.5,
        ge=0,
        le=1,
        description='The effective area for air flow at the bottom of the shade, divided'
        ' by the horizontal area between glass and shade.'
    )

    left_opening_multiplier: float = Field(
        0.5,
        ge=0,
        le=1,
        description='The effective area for air flow at the left side of the shade,'
        ' divided by the vertical area between glass and shade.'
    )

    right_opening_multiplier: float = Field(
        0.5,
        ge=0,
        le=1,
        description='The effective area for air flow at the right side of the shade,'
        ' divided by the vertical area between glass and shade.'
    )
