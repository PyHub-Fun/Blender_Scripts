import imp
import visBPY as vis

imp.reload(vis)


def main():
    print(vis.make_data_scatter(10))
    vis.remove_objects()


main()
