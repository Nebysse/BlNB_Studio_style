PROJECT_SCHEMAS = {
    "single_shot": {
        "root_name_pattern": "{project_code}",
        "directories": {
            "00_admin": {
                "docs": {},
                "spreadsheets": {},
                "mgmt": {},
            },
            "01_assets": {
                "char": {},
                "prop": {},
                "env": {},
                "fx": {},
                "veh": {},
                "veg": {},
                "light": {},
            },
            "02_shots": {
                "sh_0001": {
                    "work": {},
                    "publish": {},
                    "cache": {},
                    "render": {},
                },
            },
            "03_edit": {
                "audio": {},
                "timelines": {},
            },
            "04_renders": {
                "preview": {},
                "final": {},
            },
            "05_lib": {
                "textures": {},
                "hdri": {},
                "scripts": {},
                "fonts": {},
            },
            "90_temp": {},
            "prod": {},
        },
        "files": [
            "prod/project_overview_v001.blend",
            "prod/project_settings.json",
            "00_admin/docs/README_project_structure.md",
        ],
    },
    "short_film": {
        "root_name_pattern": "{project_code}",
        "directories": {
            "00_admin": {
                "docs": {},
                "spreadsheets": {},
                "mgmt": {},
            },
            "01_assets": {
                "char": {},
                "prop": {},
                "env": {},
                "fx": {},
                "veh": {},
                "veg": {},
                "light": {},
            },
            "02_shots": {
                "seq_010": {
                    "sh_0010": {
                        "work": {},
                        "publish": {},
                        "cache": {},
                        "render": {},
                    },
                },
            },
            "03_edit": {
                "audio": {},
                "timelines": {},
            },
            "04_renders": {
                "preview": {},
                "final": {},
            },
            "05_lib": {
                "textures": {},
                "hdri": {},
                "scripts": {},
                "fonts": {},
            },
            "90_temp": {},
            "prod": {},
        },
        "files": [
            "prod/project_overview_v001.blend",
            "prod/project_settings.json",
            "00_admin/docs/README_project_structure.md",
        ],
    },
    "asset_library": {
        "root_name_pattern": "{project_code}",
        "directories": {
            "00_admin": {
                "docs": {},
                "spreadsheets": {},
                "mgmt": {},
            },
            "01_assets": {
                "char": {},
                "prop": {},
                "env": {},
                "fx": {},
                "veh": {},
                "veg": {},
                "light": {},
            },
            "05_lib": {
                "textures": {},
                "hdri": {},
                "scripts": {},
                "fonts": {},
            },
            "90_temp": {},
            "prod": {},
        },
        "files": [
            "prod/project_overview_v001.blend",
            "prod/project_settings.json",
            "00_admin/docs/README_project_structure.md",
        ],
    },
}

ASSET_TEMPLATES = {
    "char": {
        "directories": {
            "work": {},
            "publish": {},
            "render": {},
        },
        "files": [
            "work/{asset_id}_layout_v001.blend",
        ],
    },
    "prop": {
        "directories": {
            "work": {},
            "publish": {},
            "render": {},
        },
        "files": [
            "work/{asset_id}_model_v001.blend",
        ],
    },
    "env": {
        "directories": {
            "work": {},
            "publish": {},
            "render": {},
        },
        "files": [
            "work/{asset_id}_layout_v001.blend",
        ],
    },
    "fx": {
        "directories": {
            "work": {},
            "publish": {},
            "cache": {},
        },
        "files": [
            "work/{asset_id}_setup_v001.blend",
        ],
    },
    "veh": {
        "directories": {
            "work": {},
            "publish": {},
            "render": {},
        },
        "files": [
            "work/{asset_id}_model_v001.blend",
        ],
    },
    "veg": {
        "directories": {
            "work": {},
            "publish": {},
            "render": {},
        },
        "files": [
            "work/{asset_id}_model_v001.blend",
        ],
    },
    "light": {
        "directories": {
            "work": {},
            "publish": {},
            "render": {},
        },
        "files": [
            "work/{asset_id}_setup_v001.blend",
        ],
    },
}

SHOT_TEMPLATES = {
    "directories": {
        "work": {},
        "publish": {},
        "cache": {},
        "render": {},
    },
    "files": [
        "work/shot_{shot_id}_layout_v001.blend",
    ],
}

