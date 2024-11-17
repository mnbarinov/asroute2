#!/usr/bin/env python3

import subprocess
import ipaddress
import sys

def fetch_routes(as_number):
    """Получение списка сетей через whois."""
    try:
        result = subprocess.run(
            ['whois', '-h', 'whois.radb.net', f' -i origin AS{as_number}'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        if result.returncode != 0 or not result.stdout:
            print(f"Ошибка выполнения whois: {result.stderr}")
            return []

        routes = []
        for line in result.stdout.splitlines():
            if line.lower().startswith("route:"):
                network = line.split(":")[1].strip()
                try:
                    routes.append(ipaddress.ip_network(network))
                except ValueError:
                    print(f"Неверный формат сети: {network}")
        return routes
    except FileNotFoundError:
        print("Команда whois не найдена. Убедитесь, что она установлена.")
        return []

def merge_networks(networks, tolerance):
    """Итеративное объединение сетей с учетом допуска."""
    networks = sorted(networks)  # Сортируем сети
    merged = networks[:]

    while True:
        new_merged = []
        skip = set()

        for i, net1 in enumerate(merged):
            if i in skip:
                continue

            combined = False
            for j, net2 in enumerate(merged[i + 1:], start=i + 1):
                if j in skip:
                    continue

                # Проверяем, можно ли объединить net1 и net2
                supernet = net1.supernet(new_prefix=net1.prefixlen - 1)
                if net2.subnet_of(supernet):
                    address_diff = abs(net2.num_addresses - net1.num_addresses)
                    if address_diff <= tolerance:
                        new_merged.append(supernet)
                        skip.update({i, j})
                        combined = True
                        break

            if not combined:
                new_merged.append(net1)

        # Если после прохода ничего не изменилось, выходим
        if len(new_merged) == len(merged):
            break

        merged = sorted(new_merged)

    return merged

def filter_nested_networks(networks):
    """Удаляет сети, вложенные в более крупные."""
    filtered = []
    for net in networks:
        if not any(net != other and net.subnet_of(other) for other in networks):
            filtered.append(net)
    return filtered

def print_usage():
    """Печатает инструкцию."""
    usage_text = """
Инструкция:
Используйте скрипт для получения маршрутов автономной системы (AS) и их укрупнения.

Пример запуска:
  asroute2 15169
  asroute2 15169 --tolerance 8

Аргументы:
  as_number    Номер автономной системы (например, 15169).
  --tolerance  Допустимое количество пропущенных сетей для объединения (по умолчанию 0).

Example usage in English:
  asroute2 15169
  asroute2 15169 --tolerance 8
"""
    print(usage_text)

def main():
    import argparse

    if len(sys.argv) == 1:
        print_usage()
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Получить сети для AS и укрупнить их.")
    parser.add_argument("as_number", type=str, help="Номер автономной системы (AS).")
    parser.add_argument(
        "--tolerance", type=int, default=0,
        help="Допустимое количество пропущенных сетей для объединения (по умолчанию 0)."
    )
    args = parser.parse_args()

    print(f"Получение маршрутов для AS{args.as_number}...")
    routes = fetch_routes(args.as_number)
    if not routes:
        print(f"Для AS{args.as_number} маршруты не найдены.")
        return

    print("Объединение сетей...")
    merged_routes = merge_networks(routes, args.tolerance)
    filtered_routes = filter_nested_networks(merged_routes)

    print("Объединённые сети:")
    for net in filtered_routes:
        print(net)

if __name__ == "__main__":
    main()
