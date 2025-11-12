#!/usr/bin/env python3
"""
Remove all `build` keys from a docker-compose YAML file and write a new file.

Usage:
  python3 scripts/remove-build-contexts.py docker-compose.yml docker-compose.nobuild.yml

This is useful when deploying to platforms (like Coolify) that do not have the
local build contexts available. The script keeps the `image` keys intact and
removes `build` entries so Compose will not attempt to build images from local
folders.

Note: requires PyYAML. Install with `pip3 install pyyaml`.
"""
import sys
import yaml


def load(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def dump(data, path):
    with open(path, "w") as f:
        yaml.safe_dump(data, f, sort_keys=False)


def remove_builds(compose):
    if not isinstance(compose, dict):
        return compose
    services = compose.get("services")
    if isinstance(services, dict):
        for name, svc in services.items():
            if isinstance(svc, dict) and "build" in svc:
                svc.pop("build", None)
                # If build was the only key, keep the service (must have image or other keys)
    return compose


def main():
    if len(sys.argv) != 3:
        print(
            "Usage: remove-build-contexts.py <in-compose.yml> <out-compose-no-build.yml>"
        )
        sys.exit(2)

    in_path = sys.argv[1]
    out_path = sys.argv[2]

    comp = load(in_path)
    comp2 = remove_builds(comp)
    dump(comp2, out_path)
    print(f"Wrote {out_path} (removed build contexts)")


if __name__ == "__main__":
    main()
