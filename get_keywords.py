import argparse

query_image_path = "~/Downloads/hogehoge.png"

methods = ["similarity_search", "classifier_prediction" "direct_generation"]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--image",
        type=str,
        required=True,
        help="path of query image",
    )
    parser.add_argument(
        "--method",
        type=str,
        required=True,
        help="how to get Keywords",
    )
    args = parser.parse_args()

    if args.method == methods[0]:
        pass
    elif args.method == methods[1]:
        pass
    else:
        print(methods)
        exit()
