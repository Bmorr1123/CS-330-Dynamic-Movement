import main
import animated_plotter

if __name__ == '__main__':
    program_name = main.main()
    animated_plotter.render(program_name, True, 250)
