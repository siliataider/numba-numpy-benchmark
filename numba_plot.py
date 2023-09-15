import ROOT
import csv
import array

csv_file = '/home/siliataider/Documents/silia-dev-root-project-folder/Benchmarking/numba_average_results.csv'

threads = []

real_time_loop_avg = []
real_time_loop_median = []
cpu_time_loop_avg = []
cpu_time_loop_median = []
real_time_loop_diff = []
cpu_time_loop_diff = []

real_time_numpy_avg = []
real_time_numpy_median = []
cpu_time_numpy_avg = []
cpu_time_numpy_median = []
real_time_numpy_diff = []
cpu_time_numpy_diff = []

c1 = ROOT.TCanvas("c1", "Real Time Benchmarking", 800, 600)
c1.SetGrid()
c2 = ROOT.TCanvas("c2", "CPU Time Benchmarking", 800, 600)
c2.SetGrid()
c3 = ROOT.TCanvas("c3", "Speedup Benchmarking", 800, 600)
c3.SetGrid()
c4 = ROOT.TCanvas("c4", "Relative Speedup Benchmarking", 800, 600)
c4.SetGrid()

with open(csv_file, mode='r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        threads.append(int(row[0]))

        real_time_loop_avg.append(float(row[1]))
        real_time_loop_median.append(float(row[2]))
        cpu_time_loop_avg.append(float(row[3]))
        cpu_time_loop_median.append(float(row[4]))

        real_time_numpy_avg.append(float(row[5]))
        real_time_numpy_median.append(float(row[6]))
        cpu_time_numpy_avg.append(float(row[7]))
        cpu_time_numpy_median.append(float(row[8]))

        real_time_loop_diff.append(abs(float(row[1]) - float(row[2])))
        real_time_numpy_diff.append(abs(float(row[5]) - float(row[6])))

        cpu_time_loop_diff.append(abs(float(row[1]) - float(row[2])))
        cpu_time_numpy_diff.append(abs(float(row[5]) - float(row[6])))

loop_factors = [float("{:.2f}".format(real_time_loop_avg[0] / time)) for time in real_time_loop_avg]
numpy_factors = [float("{:.2f}".format(real_time_numpy_avg[0] / time)) for time in real_time_numpy_avg]
numpy_factors_relative_to_loop = [float("{:.2f}".format(real_time_loop_avg[0] / time)) for time in real_time_numpy_avg]

graph_avg_loop = ROOT.TGraphErrors(len(threads), array.array('d', threads), array.array('d', real_time_loop_avg), 0, array.array('d', real_time_loop_diff))
graph_avg_numpy = ROOT.TGraphErrors(len(threads), array.array('d', threads), array.array('d', real_time_numpy_avg), 0, array.array('d', real_time_numpy_diff))

graph_avg_cpu_loop = ROOT.TGraphErrors(len(threads), array.array('d', threads), array.array('d', cpu_time_loop_avg), 0, array.array('d', cpu_time_loop_diff))
graph_avg_cpu_numpy = ROOT.TGraphErrors(len(threads), array.array('d', threads), array.array('d', cpu_time_numpy_avg), 0, array.array('d', cpu_time_numpy_diff))

graph_factors_loop = ROOT.TGraph(len(threads), array.array('d', threads), array.array('d', loop_factors))
graph_factors_numpy = ROOT.TGraph(len(threads), array.array('d', threads), array.array('d', numpy_factors))
graph_factors_numpy_relative_to_loop = ROOT.TGraph(len(threads), array.array('d', threads), array.array('d', numpy_factors_relative_to_loop))

c1.cd()
graph_avg_loop.SetTitle("Average Real Time (Loop vs Numpy)")
graph_avg_loop.SetLineColor(ROOT.kRed)
graph_avg_loop.GetXaxis().SetTitle("Threads")
graph_avg_loop.GetYaxis().SetTitle("Average Real Time (s)")
graph_avg_loop.GetYaxis().SetRangeUser(0, 100)

graph_avg_numpy.SetLineColor(ROOT.kBlue)

graph_avg_loop.Draw("APL")
graph_avg_numpy.Draw("PL")

legend1 = ROOT.TLegend(0.65, 0.65, 0.85, 0.85)
legend1.AddEntry(graph_avg_loop, "Loop", "lp")
legend1.AddEntry(graph_avg_numpy, "Numpy", "lp")
legend1.Draw()

c2.cd()
graph_avg_cpu_loop.SetTitle("Average CPU Time (Loop vs Numpy)")
graph_avg_cpu_loop.SetLineColor(ROOT.kRed)
graph_avg_cpu_loop.GetXaxis().SetTitle("Threads")
graph_avg_cpu_loop.GetYaxis().SetTitle("Average CPU Time (s)")
graph_avg_cpu_loop.GetYaxis().SetRangeUser(0, 100)

graph_avg_cpu_numpy.SetLineColor(ROOT.kBlue)

graph_avg_cpu_loop.Draw("APL")
graph_avg_cpu_numpy.Draw("PL")

legend2 = ROOT.TLegend(0.65, 0.35, 0.85, 0.55)
legend2.AddEntry(graph_avg_cpu_loop, "Loop", "lp")
legend2.AddEntry(graph_avg_cpu_numpy, "Numpy", "lp")
legend2.Draw()

c3.cd()
graph_factors_loop.SetTitle("Speedup Time (Loop vs Numpy)")
graph_factors_loop.SetLineColor(ROOT.kRed)
graph_factors_loop.GetXaxis().SetTitle("Threads")
graph_factors_loop.GetYaxis().SetTitle("Speedup factor")
graph_factors_loop.GetYaxis().SetRangeUser(0, 10)
graph_factors_loop.SetMarkerStyle(20)
graph_factors_loop.SetMarkerColor(ROOT.kRed)
graph_factors_loop.SetLineWidth(2)

graph_factors_numpy.SetLineColor(ROOT.kBlue)
graph_factors_numpy.SetMarkerStyle(21)
graph_factors_numpy.SetMarkerColor(ROOT.kBlue)
graph_factors_numpy.SetLineWidth(2)

graph_factors_loop.Draw("APL")
graph_factors_numpy.Draw("PL")

legend3 = ROOT.TLegend(0.15, 0.55, 0.35, 0.75)
legend3.AddEntry(graph_factors_loop, "Loop", "lp")
legend3.AddEntry(graph_factors_numpy, "Numpy", "lp")
legend3.Draw()

c4.cd()
graph_factors_loop.SetTitle("Speedup Time (Loop vs Numpy)")
graph_factors_loop.SetLineColor(ROOT.kRed)
graph_factors_loop.GetXaxis().SetTitle("Threads")
graph_factors_loop.GetYaxis().SetTitle("Speedup factor")
graph_factors_loop.GetYaxis().SetRangeUser(0, 10)
graph_factors_loop.SetMarkerStyle(20)
graph_factors_loop.SetMarkerColor(ROOT.kRed)
graph_factors_loop.SetLineWidth(2)

graph_factors_numpy_relative_to_loop.SetLineColor(ROOT.kBlue)
graph_factors_numpy_relative_to_loop.SetMarkerStyle(21)
graph_factors_numpy_relative_to_loop.SetMarkerColor(ROOT.kBlue)
graph_factors_numpy_relative_to_loop.SetLineWidth(2)

graph_factors_loop.Draw("APL")
graph_factors_numpy_relative_to_loop.Draw("PL")

legend4 = ROOT.TLegend(0.15, 0.55, 0.35, 0.75)
legend4.AddEntry(graph_factors_loop, "Loop", "lp")
legend4.AddEntry(graph_factors_numpy_relative_to_loop, "Numpy", "lp")
legend4.Draw()


c1.SaveAs("/home/siliataider/Documents/silia-dev-root-project-folder/Benchmarking/Numba Benchmarks/numba_benchmark_real_time_avg.png")
c2.SaveAs("/home/siliataider/Documents/silia-dev-root-project-folder/Benchmarking/Numba Benchmarks/numba_benchmark_cpu_time_avg.png")
c3.SaveAs("/home/siliataider/Documents/silia-dev-root-project-folder/Benchmarking/Numba Benchmarks/numba_benchmark_speedup_avg.png")
c4.SaveAs("/home/siliataider/Documents/silia-dev-root-project-folder/Benchmarking/Numba Benchmarks/numba_benchmark_relative_speedup_avg.png")
