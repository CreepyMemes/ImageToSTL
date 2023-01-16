$fa = 1;
$fs = 0.4;

img_width = 157;
img_height = 192;

back_thickness = 5;
base_width = img_width;
base_depth = 30;
base_thickness = 2;

translate([0, 0, base_thickness + img_height/2]) rotate([90, 0, 0]) {
    scale([1, 1, 0.125]) surface("dwayne-3d.png", center = true);

    translate([0, 0, -0.5*back_thickness]) cube([img_width, img_height, back_thickness], center=true);
}

translate([0, -base_depth/2+back_thickness, base_thickness/2]) cube([base_width, base_depth, base_thickness], center=true);
